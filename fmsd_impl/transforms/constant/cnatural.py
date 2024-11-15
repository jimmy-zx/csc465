from typing import Callable

from fmsd.ast import VarNode
from fmsd.ast.node import Node
from fmsd.transform.transform import SymmetricFunctionTransform
from fmsd_impl.constants import INFINITY, INT, NAT, ONE, RAT, REAL, TRUE, XINT, XREAL
from fmsd_impl.operators import (
    BunchInterval,
    DividedBy,
    GreaterThan,
    GreaterThanOrEqualsTo,
    In,
    LessThan,
    LessThanOrEqualsTo,
    Max,
    Min,
    Minus,
    Multiply,
    Plus,
    Power,
)
from fmsd_impl.transforms.ctype import to_bin, to_natural


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
def t_natural_limit(src: Node, dst: Node) -> bool:
    if src != TRUE:
        return False
    x = VarNode("x")
    if (vt := ((-INFINITY < x) & (x < INFINITY)).match(dst, {})) is not None:
        if to_natural(vt[x]) is None:
            return False
        return True
    if (vt := (-INFINITY < x).match(dst, {})) is not None:
        if to_natural(vt[x]) is None:
            return False
        return True
    if (vt := (x < INFINITY).match(dst, {})) is not None:
        if to_natural(vt[x]) is None:
            return False
        return True
    return False


@SymmetricFunctionTransform
def t_natural(src: Node, dst: Node) -> bool:
    if src != TRUE:
        return False
    x = VarNode("x")
    y = VarNode("y")
    if (vt := In(x, y).match(dst, {})) is None:
        return False
    if to_natural(vt[x]) is None:
        return False
    if vt[y] not in (
        NAT,
        INT,
        RAT,
        REAL,
        XINT,
        XREAL,
    ):
        return False
    return True


@SymmetricFunctionTransform
def t_natural_range(src: Node, dst: Node) -> bool:
    x = VarNode("x")
    l = VarNode("l")
    r = VarNode("r")
    if (vt := In(x, BunchInterval(l, r)).match(dst, {})) is None:
        return False
    if (xv := to_natural(vt[x])) is None:
        return False
    if (lv := to_natural(vt[l])) is None:
        return False
    if (rv := to_natural(vt[r])) is None:
        return False
    return to_bin(src) == (lv <= xv < rv)


def map_natural_op(
    op: type[Node], func: Callable[[int, int, int], bool]
) -> Callable[[Node, Node], bool]:
    def wrapper(src: Node, dst: Node) -> bool:
        l = VarNode("l")
        r = VarNode("r")
        if (vt := op(l, r).match(src, {})) is None:
            return False
        if (lv := to_natural(vt[l])) is None:
            return False
        if (rv := to_natural(vt[r])) is None:
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
t_natural_max = SymmetricFunctionTransform(
    map_natural_op(Max, lambda x, y, r: max(x, y) == r)
)
t_natural_min = SymmetricFunctionTransform(
    map_natural_op(Min, lambda x, y, r: min(x, y) == r)
)
t_natural_pow = SymmetricFunctionTransform(
    map_natural_op(Power, lambda x, y, r: pow(x, y) == r)
)


def map_natural_binop(
    op: type[Node], func: Callable[[int, int, bool], bool]
) -> Callable[[Node, Node], bool]:
    def wrapper(src: Node, dst: Node) -> bool:
        l = VarNode("l")
        r = VarNode("r")
        if (vt := op(l, r).match(src, {})) is None:
            return False
        if (lv := to_natural(vt[l])) is None:
            return False
        if (rv := to_natural(vt[r])) is None:
            return False
        if (res := to_bin(dst)) is None:
            return False
        return func(lv, rv, res)

    return wrapper


t_natural_lt = SymmetricFunctionTransform(
    map_natural_binop(LessThan, lambda x, y, r: (x < y) == r)
)
t_natural_le = SymmetricFunctionTransform(
    map_natural_binop(LessThanOrEqualsTo, lambda x, y, r: (x <= y) == r)
)
t_natural_gt = SymmetricFunctionTransform(
    map_natural_binop(GreaterThan, lambda x, y, r: (x > y) == r)
)
t_natural_ge = SymmetricFunctionTransform(
    map_natural_binop(GreaterThanOrEqualsTo, lambda x, y, r: (x >= y) == r)
)
