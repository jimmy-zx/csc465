from typing import Callable, final

from fmsd.ast.node import Node, VarTable
from fmsd.ast_ext.operator import Operator
from fmsd_impl.operators.binary import And


@final
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


@final
class VTCondition(Node):
    def __init__(self, node: Node, cond: Callable[[VarTable], bool]) -> None:
        super().__init__(node)
        self.cond = cond

    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return False
        return self.nodes == other.nodes and self.cond == other.cond

    def __hash__(self):
        return hash((type(self), self.nodes[0], self.cond))

    def print(self, depth: int = 0) -> str:
        return self.nodes[0].print(depth)

    def copy(self, copy_on_construction: bool = True) -> "Node":
        return type(self)(self.nodes[0], self.cond)

    def match(self, target: "Node", vt: VarTable) -> VarTable | None:
        raise TypeError()

    def eval(self, vt: VarTable) -> "Node":
        raise TypeError()


__all__ = [
    "Context",
    "VTCondition",
]
