from fmsd.ast.node import Node
from fmsd.ast_expression.operator import Associative, Commutative
from fmsd.transform.func import FunctionTransform


def func_associative(src: Node, dst: Node) -> bool:
    if type(src) is not type(dst):
        return False
    if not isinstance(src, Associative):
        return False
    if not isinstance(src, Commutative):
        return src.flatten() == dst.flatten()
    return set(src.flatten()) == set(dst.flatten())


t_associative = FunctionTransform(func_associative)


def func_commutative(src: Node, dst: Node) -> bool:
    if type(src) is not type(dst):
        return False
    if not isinstance(src, Commutative):
        return False
    return set(src.nodes) == set(dst.nodes)


t_commutative = FunctionTransform(func_commutative)
