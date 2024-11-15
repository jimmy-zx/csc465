from fmsd.ast import Node
from fmsd.proof.proof import StepProof
from fmsd.transform.transform import Transform


class TransformProof(StepProof):
    def __init__(
        self, src: Node, dst: Node, transform: Transform, index: list[int]
    ) -> None:
        super().__init__(src, dst, (transform.name or "").rsplit("::", 1)[-1])
        self.transform = transform
        self.index = index

    def verify(self) -> bool:
        assert self.transform.verify(self.src.get(self.index), self.dst.get(self.index))
        if not self.index:
            return True
        src = self.src.replace(self.index, self.dst.get(self.index))
        assert src == self.dst
        return True

    def __eq__(self, other) -> bool:
        if not isinstance(other, TransformProof):
            return False
        return (
            self.src == other.src
            and self.dst == other.dst
            and self.transform == other.transform
            and self.index == other.index
        )
