from typing import Callable

from fmsd.ast import Node
from fmsd.ast.node import VarTable


def symbol_notin(sym: Node, target: Node) -> Callable[[VarTable], bool]:
    def wrapper(vt: VarTable) -> bool:
        return all(node != vt[sym] for node in vt[target].walk_preorder())

    return wrapper
