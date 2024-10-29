from typing import Sequence

from fmsd.ast import Node
from fmsd.proof.proof import Proof, ProofException, EquivProof


class ChainProof(Proof):
    def __init__(self, src: Node, dst: Node, proofs: Sequence[Proof]) -> None:
        Proof.__init__(self, src, dst)
        self.proofs = proofs

    def verify(self) -> bool:
        last = self.src
        for i, proof in enumerate(self.proofs):
            assert proof.src == last
            try:
                assert proof.verify()
            except Exception as ex:
                raise ProofException(f"ChainProof: failed to verify step {i}") from ex
            last = proof.dst
        assert last == self.dst
        return True

    def formalize(self) -> "Proof":
        return ChainProof(
            self.src, self.dst, [proof.formalize() for proof in self.proofs]
        )

    def __eq__(self, other):
        if not isinstance(other, ChainProof):
            return False
        return (
            self.src == other.src
            and self.dst == other.dst
            and self.proofs == other.proofs
        )

    def __str__(self) -> str:
        s = f"\n\t{self.src}"
        for proof in self.proofs:
            s += f"\t{proof.hint}\n=>\t{proof}"
        return s


class ChainEquivProof(ChainProof):
    def __init__(self, src: Node, dst: Node, proofs: Sequence[EquivProof]) -> None:
        ChainProof.__init__(self, src, dst, proofs)

    def verify(self) -> bool:
        for proof in self.proofs:
            assert isinstance(proof, EquivProof)
        return ChainProof.verify(self)

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
