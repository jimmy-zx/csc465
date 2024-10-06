from abc import ABC, abstractmethod
from typing import Sequence

from fmsd.expression import Expression


class Proof(ABC):
    def __init__(self, src: Expression, dst: Expression, hint: str = "") -> None:
        self.src = src
        self.dst = dst
        self.hint = hint

    @abstractmethod
    def verify(self, debug: bool = False) -> bool:
        ...


class EquivProof(Proof):
    def __init__(self, src: Expression, dst: Expression, fwd: Proof, bwd: Proof) -> None:
        Proof.__init__(self, src, dst, fwd.hint)
        self.fwd = fwd
        self.bwd = bwd

    def verify(self, debug: bool = False) -> bool:
        assert self.fwd.src == self.src
        assert self.fwd.dst == self.dst
        assert self.bwd.src == self.dst
        assert self.bwd.dst == self.src
        if not self.fwd.verify(debug=debug):
            if debug:
                print("fwd failed")
            return False
        if not self.bwd.verify(debug=debug):
            if debug:
                print("rev failed")
            return False
        return True

    def __str__(self) -> str:
        return str(self.fwd)


class ChainProof(Proof):
    def __init__(self, src: Expression, dst: Expression, proofs: Sequence[Proof]) -> None:
        Proof.__init__(self, src, dst)
        self.proofs = proofs

    def verify(self, debug: bool = False) -> bool:
        last = self.src
        for proof in self.proofs:
            assert proof.src == last
            assert proof.verify(debug)
            last = proof.dst
        assert last == self.dst
        return True


class EquivChainProof(EquivProof, ChainProof):
    def __init__(self, src: Expression, dst: Expression, proofs: Sequence[EquivProof]) -> None:
        ChainProof.__init__(self, src, dst, proofs)

    def verify(self, debug: bool = False) -> bool:
        for proof in self.proofs:
            assert isinstance(proof, EquivProof)
        return ChainProof.verify(self, debug)

    def __str__(self) -> str:
        s = f"\n\t{self.src}"
        for proof in self.proofs:
            s += f"\t{proof.hint}\n=\t{proof}"
        return s
