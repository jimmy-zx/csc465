import itertools

from fmsd.expression import Expression, VarTable
from fmsd.proof import Proof, ChainProof, EquivProof
from fmsd.proof.step import StepProof, Step
from fmsd.rule import MatchRule, FunctionRule, Rule
from fmsd.transform import Transform
from fmsd.transform.expr import ExpressionTransform
from fmsd.transform.transforms import t_all


class TransformProof(Proof):
    def __init__(self, src: Expression, dst: Expression, transform: Transform, index: list[int]) -> None:
        Proof.__init__(self, src, dst, transform.name or "")
        self.transform = transform
        self.index = index

    def verify(self, debug: bool = False) -> bool:
        assert self.transform.verify(self.src.get(self.index), self.dst.get(self.index))
        if not self.index:
            return True
        src = self.src.copy()
        src.set(self.index, self.dst.get(self.index))
        assert src == self.dst
        return True


class NoTransformationFoundException(Exception):
    def __init__(self, src: Expression, dst: Expression) -> None:
        diff = src.diff(dst)
        assert diff is not None
        msgs = [f"Failed to find transformation for {src.get(diff)} to {dst.get(diff)}"]
        # some trick to make the filename clickable in pycharm
        if src.stack:
            msgs.append(f"src File \"{src.stack.filename}\", line {src.stack.lineno}, {src}")
        else:
            msgs.append(f"src {src}")
        if dst.stack:
            msgs.append(f"dst File \"{dst.stack.filename}\", line {dst.stack.lineno}, {dst}")
        else:
            msgs.append(f"dst {dst}")
        Exception.__init__(self, "\n".join(msgs))


class DerivedStepProof(Proof):
    def __init__(self, src: Expression, dst: Expression) -> None:
        Proof.__init__(self, src, dst, "")
        self.derived_proof: Proof | None = None

    def verify(self, debug: bool = False) -> bool:
        idx = self.src.diff(self.dst)
        if idx is None:
            return True
        steps = []
        src = self.src
        while src != self.dst:
            if (res := self.refine_once(src, self.dst, t_all)) is None:
                idx = src.diff(self.dst)
                assert idx is not None
                raise NoTransformationFoundException(self.src, self.dst)
            steps.append(TransformProof(src, res[1], res[0], res[2]))
            src = res[1]
        self.derived_proof = ChainProof(
            self.src, self.dst, steps
        )
        try:
            assert self.derived_proof.verify()
        except Exception as ex:
            raise Exception("Failed to verify derived proof") from ex
        self.hint = self.derived_proof.hint
        return True

    def formalize(self) -> "Proof":
        if not self.derived_proof:
            assert self.verify()
        assert self.derived_proof is not None
        return self.derived_proof

    def __eq__(self, other) -> bool:
        return self.src == other.src and self.dst == other.dst

    @staticmethod
    def refine_once(src: Expression, dst: Expression, transforms: dict[str, Transform]) -> tuple[Transform, Expression, list[int]] | None:
        assert src.diff(dst) is not None
        for i in itertools.count(start=0):
            idx = src.diff(dst, start=i)
            if idx is None:
                break
            if (res := DerivedStepProof.verify_transforms(src.get(idx), dst.get(idx), src.context(idx), transforms)) is not None:
                if not idx:
                    refined = dst
                else:
                    refined = src.copy()
                    refined.set(idx, dst.get(idx))

                return res, refined, idx
        idx = src.diff(dst)
        while idx:
            idx.pop()
            if (res := DerivedStepProof.verify_transforms(src.get(idx), dst.get(idx), src.context(idx), transforms)) is not None:
                if not idx:
                    refined = dst
                else:
                    refined = src.copy()
                    refined.set(idx, dst.get(idx))

                return res, refined, idx
        return None

    @staticmethod
    def verify_transforms(src: Expression, dst: Expression, context: list[Expression], transforms: dict[str, Transform]) -> Transform | None:
        for trf in transforms.values():
            if trf.verify(src, dst):
                return trf
        for ctx in context:
            trf = ExpressionTransform(ctx)
            trf.name = "context"
            if trf.verify(src, dst):
                return trf
        return None


class DerivedChainProof(ChainProof):
    def __init__(self, src: Expression, dst: Expression, steps: list[Expression]) -> None:
        ChainProof.__init__(self, src, dst, [
            DerivedStepProof(steps[i], steps[i + 1])
            for i in range(len(steps) - 1)
        ])


class DerivedEquivChainProof(EquivProof):
    def __init__(self, src: Expression, dst: Expression, steps: list[Expression]) -> None:
        EquivProof.__init__(
            self,
            src, dst,
            DerivedChainProof(src, dst, steps),
            DerivedChainProof(dst, src, steps[::-1])
        )
