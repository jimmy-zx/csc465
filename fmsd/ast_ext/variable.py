from typing import final

from fmsd.ast import VarNode
from fmsd.ast.node import Node, VarTable


@final
class Variable(Node):
    def __init__(self, *args, **kwargs) -> None:
        if "name" in kwargs:
            assert len(kwargs) == 1
            name = kwargs["name"]
        elif len(args) == 1:
            name = args[0]
        else:
            assert False, "`name` is required for argument"
        super().__init__(name=name)

    def print(self, depth: int) -> str:
        return self.meta["name"]

    def eval(self, vt: VarTable) -> "Node":
        return vt.get(self, self)

    @staticmethod
    def sym_refs(node: Node) -> set[Node]:
        if isinstance(node, (VarNode, Variable)):
            return {node}
        return (
            set().union(*(Variable.sym_refs(node) for node in node.nodes))
            - node.sym_decls()
        )


def func_init_symbols(self: Node) -> None:
    decls = set().union(*(node.sym_decls() for node in self.nodes))
    for node in self.nodes:
        assert not decls.intersection(Variable.sym_refs(node))


Node._init_symbols = func_init_symbols  # pylint: disable=protected-access
