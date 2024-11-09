from fmsd.ast.node import Node
from fmsd.ast_ext.operator import Operator
from fmsd_impl.operators.binary import And


class Context(Operator):
    N = 2

    def print(self, depth: int = 0) -> str:
        return f"Context({self.nodes[0].print(depth + 1)},{self.nodes[1].print(depth + 1)})"

    def context(self) -> list["Node"]:
        theorems = [self.nodes[1]]
        if isinstance(self.nodes[1], And):
            theorems.extend(self.nodes[1].flatten())
        if self.parent is not None:
            theorems.extend(self.parent.context())
        return theorems


__all__ = [
    "Context",
]
