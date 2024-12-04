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

    @staticmethod
    def sym_decl_all(node: Node, include_self: bool = True) -> set[Node]:
        base = set()
        if include_self:
            base = node.sym_decls()
        return base.union(*(Variable.sym_decl_all(node, True) for node in node.nodes))

    @staticmethod
    def sym_avail(node: Node, idx: list[int]) -> set[Node]:
        syms = node.sym_decls()
        if idx:
            syms = syms.union(Variable.sym_avail(node.nodes[idx[0]], idx[1:]))
        return syms


def func_init_symbols(self: Node) -> None:
    decls = Variable.sym_decl_all(self, include_self=False)
    for node in self.nodes:
        res = decls.intersection(Variable.sym_refs(node))
        assert not res


Node._init_symbols = func_init_symbols  # pylint: disable=protected-access
