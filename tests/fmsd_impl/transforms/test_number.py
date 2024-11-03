import operator
import random
from typing import Callable

import pytest

import fmsd_impl.patch
from fmsd.ast import Node
from fmsd.ast_ext import Constant
from fmsd.proof import DerivedEquivChainProof
from fmsd_impl.constants import INFINITY, NAT, ONE, TRUE, ZERO
from fmsd_impl.operators import (
    Context,
    DividedBy,
    Equals,
    Implies,
    In,
    Minus,
    Multiply,
    Plus,
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
            Implies((TRUE & TRUE) & TRUE, Equals(ONE - ONE, ZERO)),
            Implies(
                ((-INFINITY < ZERO) & (ZERO < ONE)) & (ONE < INFINITY),
                Equals(ONE - ONE, ZERO),
            ),
            Implies((-INFINITY < ONE) & (ONE < INFINITY), Equals(ONE - ONE, ZERO)),
            TRUE,
        ],
    )
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
    ],
)
def test_natural_closed_op(op: type[Node], func: Callable[[int, int], int]):
    r = random.randint(0, 2**16)
    l = r * random.randint(1, 2**16)
    assert DerivedEquivChainProof(
        op(Constant(str(l)), Constant(str(r))),
        Constant(str(func(l, r))),
        [
            op(Constant(str(l)), Constant(str(r))),
            Constant(str(func(l, r))),
        ],
    ).verify()
