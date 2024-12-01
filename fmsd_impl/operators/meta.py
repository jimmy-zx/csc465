from typing import final

from fmsd.ast.node import Node
from fmsd.impl.operators import Context, VTCondition


@final
class SymbolDeclaration(Node):
    N = 2

    def _init_sym_decl(self) -> None:
        assert self.nodes[0] not in self.nodes[1].sym_decls()

    def print(self, depth: int) -> str:
        return self.nodes[1].print(depth)

    def sym_decls(self) -> set["Node"]:
        return super().sym_decls().union({self.nodes[0]})


__all__ = [
    "Context",
    "VTCondition",
    "SymbolDeclaration",
]
