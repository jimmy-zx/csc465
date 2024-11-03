from typing import Self, final

from fmsd.ast.base import CopyOnConstruction
from fmsd.ast.node import Node, VarTable


@final
class Constant(Node, CopyOnConstruction):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash((type(self), self.name))

    def print(self, depth: int = 0) -> str:
        return self.name

    def copy(self) -> Self:
        return type(self)(self.name)

    def match(self, target: "Node", vt: VarTable) -> VarTable | None:
        if self == target:
            return vt
        return None

    def eval(self, vt: VarTable) -> "Node":
        return self.copy()
