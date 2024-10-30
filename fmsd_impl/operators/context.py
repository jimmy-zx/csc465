from fmsd.ast.node import Node
from fmsd.ast_ext.operator import Operator


class Context(Operator):
    N = 2

    def print(self, depth: int = 0) -> str:
        return f"Context({self.nodes[0].print(depth + 1)},{self.nodes[1].print(depth + 1)})"

    def context(self) -> list["Node"]:
        return [self.nodes[1]] + (
            self.parent.context() if self.parent is not None else []
        )
