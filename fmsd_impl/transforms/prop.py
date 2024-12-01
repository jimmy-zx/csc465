from collections import Counter

from fmsd.ast.node import Node
from fmsd.transform.transform import SymmetricFunctionTransform
from fmsd_impl.operators import Associative, Commutative, Idempotent


@SymmetricFunctionTransform
def t_associative(src: Node, dst: Node) -> bool:
    if type(src) is not type(dst):
        return False
    if not Associative.has_prop(type(src)):
        return False
    if not Commutative.has_prop(type(src)):
        return src.flatten() == dst.flatten()
    if not Idempotent.has_prop(type(src)):
        return Counter(src.flatten()) == Counter(dst.flatten())
    return set(src.flatten()) == set(dst.flatten())


@SymmetricFunctionTransform
def t_commutative(src: Node, dst: Node) -> bool:
    if type(src) is not type(dst):
        return False
    if not Commutative.has_prop(type(src)):
        return False
    return src.nodes[1] == dst.nodes[0] and dst.nodes[1] == src.nodes[0]


@SymmetricFunctionTransform
def t_idempotent(src: Node, dst: Node) -> bool:
    if not Idempotent.has_prop(type(src)):
        return False
    elem = set(src.flatten())
    if len(elem) != 1:
        return False
    return elem == {dst}
