from fmsd.ast.node import Node
from fmsd.ast_ext.operator import Operator


class Context(Operator):
    N = 2

    def __str__(self) -> str:
        return f"Context({self.nodes[0]},{self.nodes[1]})"

    def context(self) -> list["Node"]:
        return [self.nodes[1]] + (
            self.parent.context() if self.parent is not None else []
        )
