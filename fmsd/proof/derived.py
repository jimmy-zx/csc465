from fmsd.ast.node import Node
from fmsd.proof.chain import ChainProof
from fmsd.proof.proof import EquivProof, Proof, ProofException, StepProof
from fmsd.proof.transform import TransformProof
from fmsd.transform import TransformManager
from fmsd.transform.transform import Transform
from fmsd.utils.impl import impl


class NoTransformationFoundException(Exception):
    def __init__(self, src: Node, dst: Node) -> None:
        diff = src.diff(dst)
        assert diff is not None
        msgs = [f"Failed to find transformation for {src.get(diff)} to {dst.get(diff)}"]
        # some trick to make the filename clickable in pycharm
        if src.stack:
            msgs.append(
                f'src File "{src.stack.filename}", line {src.stack.lineno}, {src}'
            )
        else:
            msgs.append(f"src {src}")
        if dst.stack:
            msgs.append(
                f'dst File "{dst.stack.filename}", line {dst.stack.lineno}, {dst}'
            )
        else:
            msgs.append(f"dst {dst}")
        Exception.__init__(self, "\n".join(msgs))


class DerivedStepProof(StepProof):
    def __init__(self, src: Node, dst: Node) -> None:
        super().__init__(src, dst, "")
        self.derived_proof: Proof | None = None

    def verify(self) -> bool:
        assert impl is not None
        idx = self.src.diff(self.dst)
        if idx is None:
            return True
        steps = []
        src = self.src
        while src != self.dst:
            if (
                res := self.refine_once(src, self.dst, impl.transform_manager())
            ) is None:
                idx = src.diff(self.dst)
                assert idx is not None
                raise NoTransformationFoundException(self.src, self.dst)
            steps.append(TransformProof(src, res[1], res[0], res[2]))
            src = res[1]
        self.derived_proof = ChainProof(self.src, self.dst, steps)
        try:
            assert self.derived_proof.verify()
        except Exception as ex:
            raise ProofException("Failed to verify derived proof") from ex
        self.hint = self.derived_proof.hint
        return True

    def formalize(self) -> "Proof":
        if self.derived_proof is None:
            assert self.verify()
        assert self.derived_proof is not None
        return self.derived_proof

    def __eq__(self, other) -> bool:
        if not isinstance(other, DerivedStepProof):
            return False
        return self.src == other.src and self.dst == other.dst

    @staticmethod
    def refine_once(
        src: Node, dst: Node, transform_manager: TransformManager
    ) -> tuple[Transform, Node, list[int]] | None:
        idx = src.diff(dst)
        end = src.weak_diff(dst)
        assert idx is not None
        assert end is not None
        while True:
            if (
                res := DerivedStepProof.verify_transforms(
                    src.get(idx),
                    dst.get(idx),
                    src.context(idx),
                    transform_manager,
                )
            ) is not None:
                return res, src.replace(idx, dst.get(idx)), idx

            if len(idx) == len(end):
                break
            idx.append(end[len(idx)])
        idx = src.diff(dst)
        assert idx is not None
        while True:
            if (
                res := DerivedStepProof.verify_transforms(
                    src.get(idx),
                    dst.get(idx),
                    src.context(idx),
                    transform_manager,
                )
            ) is not None:
                return res, src.replace(idx, dst.get(idx)), idx
            if not idx:
                break
            idx.pop()
        return None

    @staticmethod
    def verify_transforms(
        src: Node, dst: Node, context: list[Node], transform_manager: TransformManager
    ) -> Transform | None:
        assert impl is not None
        for i, trf in enumerate(transform_manager):
            if trf.verify(src, dst):
                transform_manager.hit(trf, i)
                return trf
        for ctx in context:
            trf = impl.node_to_transform(ctx)
            trf.name = "context"
            if trf.verify(src, dst):
                return trf
        return None


class DerivedChainProof(ChainProof):
    def __init__(self, src: Node, dst: Node, steps: list[Node]) -> None:
        ChainProof.__init__(
            self,
            src,
            dst,
            [DerivedStepProof(steps[i], steps[i + 1]) for i in range(len(steps) - 1)],
        )


class DerivedEquivChainProof(EquivProof):
    def __init__(self, src: Node, dst: Node, steps: list[Node]) -> None:
        EquivProof.__init__(
            self,
            src,
            dst,
            DerivedChainProof(src, dst, steps),
            DerivedChainProof(dst, src, steps[::-1]),
        )


class DynamicProofFactory:
    def __init__(self, steps: list[Node] | None = None) -> None:
        self.steps = steps or []

    def s(self, node: Node) -> None:
        self.steps.append(node)

    def generate(self, cls) -> Proof:
        return cls(self.steps[0], self.steps[-1], self.steps)
