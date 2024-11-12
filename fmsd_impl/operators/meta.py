from typing import Callable, final

from fmsd.ast.node import Node, VarTable
from fmsd.ast_ext.operator import Operator
from fmsd_impl.operators.binary import And


@final
class Context(Operator):
    N = 2

    def print(self, depth: int) -> str:
        return f"Context({self.nodes[0].print(depth + 1)},{self.nodes[1].print(depth + 1)})"

    def context(self) -> list["Node"]:
        theorems = [self.nodes[1]]
        if isinstance(self.nodes[1], And):
            theorems.extend(self.nodes[1].flatten())
        if self.parent is not None:
            theorems.extend(self.parent.context())
        return theorems


@final
class SymbolDeclaration(Node):
    N = 2

    def _init_sym_decl(self) -> None:
        assert self.nodes[0] not in self.nodes[1].sym_decls()

    def print(self, depth: int) -> str:
        return self.nodes[1].print(depth)

    def sym_decls(self) -> set["Node"]:
        return super().sym_decls().union({self.nodes[0]})


@final
class VTCondition(Node):
    def __init__(self, node: Node, *, cond: Callable[[VarTable], bool]) -> None:
        super().__init__(node, cond=cond)

    def print(self, depth: int) -> str:
        return self.nodes[0].print(depth)

    def match(self, target: "Node", vt: VarTable) -> VarTable | None:
        raise TypeError()

    def eval(self, vt: VarTable) -> "Node":
        raise TypeError()


__all__ = [
    "Context",
    "VTCondition",
    "SymbolDeclaration",
]
