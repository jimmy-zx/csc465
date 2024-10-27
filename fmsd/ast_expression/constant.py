from typing import Self

from fmsd.ast.node import Node, VarTable


class Constant(Node):
    def __init__(self, name: str) -> None:
        Node.__init__(self)
        self.name = name

    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return False
        return self.name == other.name

    def __str__(self) -> str:
        return self.name

    def copy(self) -> Self:
        return type(self)(self.name)

    def match(self, target: "Node", vt: VarTable) -> VarTable | None:
        if self == target:
            return vt
        return None
