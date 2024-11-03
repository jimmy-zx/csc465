from fmsd.ast import Node
from fmsd.ast_ext import Constant


def to_natural(node: Node) -> int | None:
    if not isinstance(node, Constant):
        return False
    if not node.name:
        return False
    if not set(node.name).issubset(set("0123456789")):
        return False
    if node.name[0] == "0" and node.name != "0":
        return False
    return int(node.name)


__all__ = ["to_natural"]
