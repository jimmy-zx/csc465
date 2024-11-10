from fmsd.ast import Node
from fmsd.ast_ext import Constant
from fmsd_impl.constants import FALSE, TRUE
from fmsd_impl.operators import Join, List


def to_natural(node: Node) -> int | None:
    if not isinstance(node, Constant):
        return None
    if not node.name:
        return None
    if not set(node.name).issubset(set("0123456789")):
        return None
    if node.name[0] == "0" and node.name != "0":
        return None
    return int(node.name)


def to_bin(node: Node) -> bool | None:
    if node == TRUE:
        return True
    if node == FALSE:
        return False
    return None


def to_list(node: Node) -> list | Node:
    if not isinstance(node, List) or not isinstance(node.nodes[0], Join):
        return node
    return [to_list(child) for child in node.nodes[0].flatten()]


__all__ = ["to_natural", "to_bin", "to_list"]
