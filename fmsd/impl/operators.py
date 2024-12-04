from typing import final

from fmsd.ast import Node
from fmsd.ast.node import VarTable
from fmsd.ast_ext import Variable
from fmsd.ast_ext.operator import Operator


class Equals(Operator):
    N = 2
    DELIM = "="


class Implies(Operator):
    N = 2
    DELIM = "⇒"


class And(Operator):
    N = 2
    DELIM = "∧"


@final
class Context(Operator):
    N = 2

    def print(self, depth: int) -> str:
        return f"Context({self.nodes[0].print(depth + 1)},{self.nodes[1].print(depth + 1)})"

    @staticmethod
    def context(node: Node, idx: list[int]) -> list[Node]:
        if isinstance(node, Context):
            theorems = [node.nodes[1]]
            if isinstance(node.nodes[1], And):
                theorems.extend(node.nodes[1].flatten())
            if not idx:
                return theorems
            return theorems + Context.context(node.nodes[idx[0]], idx[1:])
        if not idx:
            return []
        return Context.context(node.nodes[idx[0]], idx[1:])


@final
class VTCondition(Node):
    def __init__(self, *args, **kwargs) -> None:
        node = args[0]
        if "cond" in kwargs:
            assert len(kwargs) == 1
            cond = kwargs["cond"]
        elif len(args) == 2:
            cond = args[1]
        else:
            assert False, "`cond` is required for argument"
        super().__init__(node, cond=cond)

    def print(self, depth: int) -> str:
        return self.nodes[0].print(depth)

    def match(self, target: "Node", vt: VarTable) -> VarTable | None:
        raise TypeError()

    def eval(self, vt: VarTable) -> "Node":
        raise TypeError()


@final
class SymbolDeclaration(Node):
    N = 2

    def _init_sym_decl(self) -> None:
        assert self.nodes[0] not in self.nodes[1].sym_decls()

    def print(self, depth: int) -> str:
        return self.nodes[1].print(depth)

    def sym_decls(self) -> set["Node"]:
        return {self.nodes[0]}


@final
class Top(Operator):
    N = 1

    def _init_top(self) -> None:
        assert not Variable.sym_refs(self.nodes[0])

    def print(self, depth: int) -> str:
        return self.nodes[0].print(depth + 1)
