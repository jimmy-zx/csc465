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

    def formalize(self) -> "Proof":
        return self


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
        try:
            assert self.fwd.verify(debug=debug)
        except Exception as ex:
            raise Exception("EquivProof: failed to verify forward") from ex
        try:
            assert self.bwd.verify(debug=debug)
        except Exception as ex:
            raise Exception("EquivProof: failed to verify forward") from ex
        return True

    def formalize(self) -> "Proof":
        return EquivProof(self.src, self.dst, self.fwd.formalize(), self.bwd.formalize())

    def __str__(self) -> str:
        return str(self.fwd)

    def __eq__(self, other) -> bool:
        if not isinstance(other, EquivProof):
            return False
        return self.src == other.src and self.dst == other.dst and self.fwd == other.fwd and self.bwd == other.bwd


class ChainProof(Proof):
    def __init__(self, src: Expression, dst: Expression, proofs: Sequence[Proof]) -> None:
        Proof.__init__(self, src, dst)
        self.proofs = proofs

    def verify(self, debug: bool = False) -> bool:
        last = self.src
        for i, proof in enumerate(self.proofs):
            assert proof.src == last
            try:
                assert proof.verify(debug)
            except Exception as ex:
                raise Exception(f"ChainProof: failed to verify step {i}") from ex
            last = proof.dst
        assert last == self.dst
        return True

    def formalize(self) -> "Proof":
        return ChainProof(self.src, self.dst, [proof.formalize() for proof in self.proofs])

    def __eq__(self, other):
        if not isinstance(other, ChainProof):
            return False
        return self.src == other.src and self.dst == other.dst and self.proofs == other.proofs

    def __str__(self) -> str:
        s = f"\n\t{self.src}"
        for proof in self.proofs:
            s += f"\t{proof.hint}\n=>\t{proof}"
        return s


class ChainEquivProof(ChainProof):
    def __init__(self, src: Expression, dst: Expression, proofs: Sequence[EquivProof]) -> None:
        ChainProof.__init__(self, src, dst, proofs)

    def verify(self, debug: bool = False) -> bool:
        for proof in self.proofs:
            assert isinstance(proof, EquivProof)
        return ChainProof.verify(self, debug)

    def formalize(self) -> "Proof":
        return ChainProof.formalize(self)

    def __str__(self) -> str:
        s = f"\n\t{self.src}"
        for proof in self.proofs:
            s += f"\t{proof.hint}\n=\t{proof}"
        return s

    def __eq__(self, other) -> bool:
        if not isinstance(other, ChainEquivProof):
            return False
        return ChainProof.__eq__(self, other)
