from abc import ABC, abstractmethod

from fmsd.expression import Expression


class Proof(ABC):
    def __init__(self, src: Expression, dst: Expression) -> None:
        self.src = src
        self.dst = dst

    @abstractmethod
    def verify(self) -> bool:
        ...


class EquivProof(Proof):
    def __init__(self, src: Expression, dst: Expression, fwd: Proof, bwd: Proof) -> None:
        Proof.__init__(self, src, dst)
        self.fwd = fwd
        self.bwd = bwd

    def verify(self) -> bool:
        assert self.fwd.src == self.src
        assert self.fwd.dst == self.dst
        assert self.bwd.src == self.dst
        assert self.bwd.dst == self.src
        return self.fwd.verify() and self.bwd.verify()


class ChainProof(Proof):
    def __init__(self, src: Expression, dst: Expression, proofs: list[Proof]) -> None:
        Proof.__init__(self, src, dst)
        self.proofs = proofs

    def verify(self) -> bool:
        last = self.src
        for proof in self.proofs:
            assert proof.src == last
            assert proof.verify()
            last = proof.dst
        assert last == self.dst
        return True


class EquivChainProof(EquivProof, ChainProof):
    def __init__(self, src: Expression, dst: Expression, proofs: list[EquivProof]) -> None:
        ChainProof.__init__(self, src, dst, proofs)

    def verify(self) -> bool:
        for proof in self.proofs:
            assert isinstance(proof, EquivProof)
        return ChainProof.verify(self)
