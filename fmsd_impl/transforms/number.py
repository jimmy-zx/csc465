from typing import Callable

from fmsd.ast import Variable
from fmsd.ast.node import Node
from fmsd.transform.transform import SymmetricFunctionTransform
from fmsd_impl.constants import INFINITY, NAT, ONE, TRUE, to_natural
from fmsd_impl.operators import DividedBy, In, Minus, Multiply, Plus


@SymmetricFunctionTransform
def t_natural_construction(src: Node, dst: Node) -> bool:
    """
    Example: 4 = 1 + 1 + 1 + 1
    """
    if (num := to_natural(src)) is None:
        return False
    if not isinstance(dst, Plus):
        return False
    nodes = dst.flatten()
    if set(nodes) != {ONE}:
        return False
    if len(nodes) != num:
        return False
    return True


@SymmetricFunctionTransform
def t_natural_range(src: Node, dst: Node) -> bool:
    if src != TRUE:
        return False
    x = Variable("x")
    if (vt := ((-INFINITY < x) & (x < INFINITY)).match(dst, {})) is None:
        return False
    if to_natural(vt["x"]) is None:
        return False
    return True


@SymmetricFunctionTransform
def t_natural(src: Node, dst: Node) -> bool:
    if src != TRUE:
        return False
    x = Variable("x")
    if (vt := In(x, NAT).match(dst, {})) is None:
        return False
    if to_natural(vt["x"]) is None:
        return False
    return True


def map_natural_op(
    op: type[Node], func: Callable[[int, int, int], bool]
) -> Callable[[Node, Node], bool]:
    def wrapper(src: Node, dst: Node) -> bool:
        l = Variable("l")
        r = Variable("r")
        if (vt := op(l, r).match(src, {})) is None:
            return False
        if (lv := to_natural(vt["l"])) is None:
            return False
        if (rv := to_natural(vt["r"])) is None:
            return False
        if (res := to_natural(dst)) is None:
            return False
        return func(lv, rv, res)

    return wrapper


t_natural_plus = SymmetricFunctionTransform(
    map_natural_op(Plus, lambda x, y, r: x + y == r)
)
t_natural_minus = SymmetricFunctionTransform(
    map_natural_op(Minus, lambda x, y, r: x - y == r)
)
t_natural_multiply = SymmetricFunctionTransform(
    map_natural_op(Multiply, lambda x, y, r: x * y == r)
)
t_natural_divided_by = SymmetricFunctionTransform(
    map_natural_op(DividedBy, lambda x, y, r: y != 0 and x / y == r)
)
