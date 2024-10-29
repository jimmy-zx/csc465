from typing import Callable

from fmsd.ast.node import Node
from fmsd.transform import Transform


class FunctionTransform(Transform):
    def __init__(self, func: Callable[[Node, Node], bool]) -> None:
        Transform.__init__(self)
        self.func = func

    def verify(self, src: Node, dst: Node) -> bool:
        return self.func(src, dst)

    def __eq__(self, other) -> bool:
        if not isinstance(other, FunctionTransform):
            return False
        return self.func == other.func
