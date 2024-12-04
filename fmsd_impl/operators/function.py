from fmsd.ast import Node
from fmsd.ast_ext import Operator, Variable


class Function(Operator):
    N = 3

    def _init_function(self) -> None:
        assert self.nodes[0] not in self.nodes[1].sym_decls()
        assert self.nodes[0] not in Variable.sym_refs(self.nodes[1])
        assert self.nodes[0] not in self.nodes[2].sym_decls()

    def print(self, depth: int = 0) -> str:
        return "<{}:{}·{}>".format(*(node.print(depth + 1) for node in self.nodes))

    def sym_decls(self) -> set["Node"]:
        return {self.nodes[0]}


class FunctionDomain(Operator):
    N = 1
    DELIM = "☐"


class FunctionSize(Operator):
    N = 1
    DELIM = "#"


class FunctionCompose(Operator):
    N = 2
    DELIM = " "


class FunctionUnion(Operator):
    N = 2
    DELIM = "|"


class FunctionTo(Operator):
    N = 2
    DELIM = "→"


__all__ = [
    "Function",
    "FunctionDomain",
    "FunctionSize",
    "FunctionCompose",
    "FunctionUnion",
    "FunctionTo",
]
