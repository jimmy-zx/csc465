import pytest

from fmsd.expression import Expression
from fmsd.expression.operators.binary import And, Or
from fmsd.expression.variables import BinaryVariable

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


@pytest.mark.parametrize(
    ("lhs", "rhs", "idx"),
    [
        (And(Or(a, b), c), And(a, c), [0]),
        (And(And(a, b), c), And(And(a, Or(a, b)), c), [0, 1]),
    ]
)
def test_symmetric_diff(lhs: Expression, rhs: Expression, idx: list[int] | None):
    assert lhs.diff(rhs) == idx
    assert rhs.diff(lhs) == idx


@pytest.mark.parametrize(
    ("lhs", "rhs"),
    [
        (And(Or(a, b), c), And(Or(a, b), c)),
    ],
)
def test_no_diff(lhs: Expression, rhs: Expression):
    assert lhs.diff(rhs) is None
    assert rhs.diff(lhs) is None


def test_start():
    lhs = And(And(a, b), c)
    rhs = And(And(Or(a, b), b), Or(a, c))
    assert lhs.diff(rhs) == []
    assert rhs.diff(lhs) == []
    assert lhs.diff(rhs, start=1) == [0, 0]
