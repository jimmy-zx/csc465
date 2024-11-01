from typing import Sequence

from fmsd.ast import Node
from fmsd.proof.proof import EquivProof, Proof, ProofException, StepProof


class ChainProof(StepProof):
    DELIM = "==>"

    def __init__(self, src: Node, dst: Node, proofs: Sequence[Proof]) -> None:
        super().__init__(src, dst, ",".join(proof.hint for proof in proofs))
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

    def steps(self) -> Sequence[Proof]:
        return self.proofs

    def __eq__(self, other):
        if not isinstance(other, ChainProof):
            return False
        return (
            self.src == other.src
            and self.dst == other.dst
            and self.proofs == other.proofs
        )


class ChainEquivProof(ChainProof):
    DELIM = "==="

    def verify(self) -> bool:
        for proof in self.proofs:
            assert isinstance(proof, EquivProof)
        return ChainProof.verify(self)

    def formalize(self) -> "Proof":
        return ChainProof.formalize(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, ChainEquivProof):
            return False
        return ChainProof.__eq__(self, other)
