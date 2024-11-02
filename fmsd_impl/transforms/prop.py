from collections import Counter

from fmsd.ast.node import Node
from fmsd.transform.transform import FunctionTransform
from fmsd_impl.operators import Associative, Commutative


def func_associative(src: Node, dst: Node) -> bool:
    if type(src) is not type(dst):
        return False
    if not isinstance(src, Associative):
        return False
    if not isinstance(src, Commutative):
        return src.flatten() == dst.flatten()
    return Counter(src.flatten()) == Counter(dst.flatten())


t_associative = FunctionTransform(func_associative)


def func_commutative(src: Node, dst: Node) -> bool:
    if type(src) is not type(dst):
        return False
    if not isinstance(src, Commutative):
        return False
    return src.nodes[1] == dst.nodes[0] and dst.nodes[1] == src.nodes[0]


t_commutative = FunctionTransform(func_commutative)
