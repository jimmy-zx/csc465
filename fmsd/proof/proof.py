import itertools
import warnings
from abc import ABC, abstractmethod

from typing_extensions import Sequence

from fmsd.ast import Node


class ProofException(Exception):
    pass


class Proof(ABC):
    def __init__(self, src: Node, dst: Node, hint: str = "") -> None:
        self.src = src
        self.dst = dst
        self.hint = hint

    @abstractmethod
    def verify(self) -> bool: ...

    def formalize(self) -> "Proof":
        return self

    def __bool__(self) -> bool:
        """
        To prevent cases like `assert Proof()`
        with missing `.verify()`
        """
        warnings.warn("Asserting proof without verify")
        return self.verify()


class StepProof(Proof, ABC):
    DELIM = "==>"

    def steps(self) -> Sequence[Proof]:
        return [self]

    def __str__(self) -> str:
        return f"\n{self.DELIM}".join(
            itertools.chain(
                (f"\t{proof.src}\t({proof.hint})" for proof in self.steps()),
                (f"\t{self.dst}",),
            )
        )

    def print(self, depth: int = 0) -> str:
        return f"\n{self.DELIM}".join(
            itertools.chain(
                (
                    f"\t{proof.src.print(depth + 1)}\t({proof.hint})"
                    for proof in self.steps()
                ),
                (f"\t{self.dst}",),
            )
        )

    def __repr__(self) -> str:
        return str(self)


class EquivProof(StepProof):
    DELIM = "==="

    def __init__(self, src: Node, dst: Node, fwd: Proof, bwd: Proof) -> None:
        super().__init__(src, dst, fwd.hint)
        self.fwd = fwd
        self.bwd = bwd

    def verify(self) -> bool:
        assert self.fwd.src == self.src
        assert self.fwd.dst == self.dst
        assert self.bwd.src == self.dst
        assert self.bwd.dst == self.src
        try:
            assert self.fwd.verify()
        except Exception as ex:
            raise ProofException("EquivProof: failed to verify forward") from ex
        try:
            assert self.bwd.verify()
        except Exception as ex:
            raise ProofException("EquivProof: failed to verify backward") from ex
        return True

    def formalize(self) -> "Proof":
        return EquivProof(
            self.src, self.dst, self.fwd.formalize(), self.bwd.formalize()
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, EquivProof):
            return False
        return (
            self.src == other.src
            and self.dst == other.dst
            and self.fwd == other.fwd
            and self.bwd == other.bwd
        )

    def steps(self) -> Sequence[Proof]:
        if hasattr(self.fwd, "steps"):
            return self.fwd.steps()
        return [self]
