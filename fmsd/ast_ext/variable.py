from typing import final

from fmsd.ast.base import CopyOnConstruction
from fmsd.ast.node import Node, VarTable


@final
class Variable(Node, CopyOnConstruction):
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
        return vt.get(self, self).copy()

    def sym_refs(self) -> set["Node"]:
        return {self}
