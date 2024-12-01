import operator
import random
from typing import Callable

import pytest

import fmsd_impl.patch
from fmsd.ast import Node
from fmsd.ast_ext import Constant
from fmsd.proof import DerivedEquivChainProof
from fmsd_impl.constants import FALSE, INFINITY, NAT, ONE, TRUE, ZERO
from fmsd_impl.operators import (
    Context,
    DividedBy,
    Equals,
    GreaterThan,
    GreaterThanOrEqualsTo,
    Implies,
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

assert fmsd_impl.patch


def test_natural_construction():
    assert DerivedEquivChainProof(
        Constant("4"),
        ONE + (ONE + ONE) + ONE,
        [
            Constant("4"),
            ONE + (ONE + ONE) + ONE,
        ],
    ).verify()
    assert DerivedEquivChainProof(
        Constant("4"),
        Constant("3") + ONE,
        [
            Constant("4"),
            ONE + (ONE + ONE + ONE),
            ONE + Constant("3"),
            Constant("3") + ONE,
        ],
    ).verify()

    assert isinstance(INFINITY, Node)
    assert DerivedEquivChainProof(
        Equals(ONE - ONE, ZERO),
        TRUE,
        [
            Equals(ONE - ONE, ZERO),
            Implies(TRUE, Equals(ONE - ONE, ZERO)),
            Implies(TRUE & TRUE, Equals(ONE - ONE, ZERO)),
            Implies((-INFINITY < ONE) & (ONE < INFINITY), Equals(ONE - ONE, ZERO)),
            TRUE,
        ],
    ).verify()
    assert DerivedEquivChainProof(
        Context(Constant("4") - ONE, Equals(ONE - ONE, ZERO)),
        Context(Constant("3"), Equals(ONE - ONE, ZERO)),
        [
            Context(Constant("4") - ONE, Equals(ONE - ONE, ZERO)),
            Context((ONE + ONE + ONE + ONE) - ONE, Equals(ONE - ONE, ZERO)),
            Context(((ONE + ONE + ONE) + ONE) - ONE, Equals(ONE - ONE, ZERO)),
            Context((ONE + ONE + ONE) + (ONE - ONE), Equals(ONE - ONE, ZERO)),
            Context((ONE + ONE + ONE) + ZERO, Equals(ONE - ONE, ZERO)),
            Context((ONE + ONE) + (ONE + ZERO), Equals(ONE - ONE, ZERO)),
            Context((ONE + ONE) + ONE, Equals(ONE - ONE, ZERO)),
            Context(Constant("3"), Equals(ONE - ONE, ZERO)),
        ],
    ).verify()


def test_natural_range():
    v = random.randint(0, 2**32)
    assert DerivedEquivChainProof(
        TRUE,
        (-INFINITY < Constant(str(v))) & (Constant(str(v)) < INFINITY),
        [
            TRUE,
            (-INFINITY < Constant(str(v))) & (Constant(str(v)) < INFINITY),
        ],
    ).verify()


def test_natural_set():
    v = random.randint(0, 2**32)
    assert DerivedEquivChainProof(
        TRUE,
        In(Constant(str(v)), NAT),
        [
            TRUE,
            In(Constant(str(v)), NAT),
        ],
    ).verify()


@pytest.mark.parametrize(
    ("op", "func"),
    [
        (Plus, operator.add),
        (Minus, operator.sub),
        (Multiply, operator.mul),
        (DividedBy, operator.floordiv),
        (Max, max),
        (Min, min),
        (Power, pow),
    ],
)
def test_natural_op(op: type[Node], func: Callable[[int, int], int]):
    r = random.randint(1, 2**8)
    l = r * random.randint(1, 2**8)
    assert DerivedEquivChainProof(
        op(Constant(str(l)), Constant(str(r))),
        Constant(str(func(l, r))),
        [
            op(Constant(str(l)), Constant(str(r))),
            Constant(str(func(l, r))),
        ],
    ).verify()


@pytest.mark.parametrize(
    ("op", "func"),
    [
        (LessThan, operator.lt),
        (LessThanOrEqualsTo, operator.le),
        (GreaterThan, operator.gt),
        (GreaterThanOrEqualsTo, operator.ge),
    ],
)
def test_natural_binop(op: type[Node], func: Callable[[int, int], bool]):
    def bool_to_bin(val: bool) -> Node:
        if val:
            return TRUE
        return FALSE

    l = random.randint(0, 2**16)
    r = random.randint(0, 2**16)

    assert DerivedEquivChainProof(
        op(Constant(str(l)), Constant(str(r))),
        bool_to_bin(func(l, r)),
        [
            op(Constant(str(l)), Constant(str(r))),
            bool_to_bin(func(l, r)),
        ],
    ).verify()

    r, l = l, r
    assert DerivedEquivChainProof(
        op(Constant(str(l)), Constant(str(r))),
        bool_to_bin(func(l, r)),
        [
            op(Constant(str(l)), Constant(str(r))),
            bool_to_bin(func(l, r)),
        ],
    ).verify()
