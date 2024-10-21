import pytest

import fmsd.utils.patch.binary
from fmsd.expression import Expression
from fmsd.expression.variables import BinaryVariable

assert fmsd.utils.patch.binary

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


@pytest.mark.parametrize(
    ("lhs", "rhs", "idx"),
    [
        ((a | b) & c, a & c, [0]),
        ((a & b) & c, (a & (a | b)) & c, [0, 1]),
        (a & b, b & a, []),
    ]
)
def test_symmetric_diff(lhs: Expression, rhs: Expression, idx: list[int] | None):
    assert lhs.diff(rhs) == idx
    assert rhs.diff(lhs) == idx


@pytest.mark.parametrize(
    ("lhs", "rhs"),
    [
        ((a | b) & c, (a | b) & c),
    ],
)
def test_no_diff(lhs: Expression, rhs: Expression):
    assert lhs.diff(rhs) is None
    assert rhs.diff(lhs) is None


def test_start():
    lhs = (a & b) & c
    rhs = ((a | b) & b) & (a | c)
    assert lhs.diff(rhs) == []
    assert rhs.diff(lhs) == []
    assert lhs.diff(rhs, start=1) == [0, 0]
    assert lhs.diff(rhs, start=3) is None


def test_mult_diff():
    lhs = (a | b) & (a | c)
    rhs = (b | a) & (b | c)
    assert lhs.diff(rhs) == []
    assert lhs.diff(rhs, 1) == [0]
