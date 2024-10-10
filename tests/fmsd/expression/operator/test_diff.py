from fmsd.expression.operators.binary import And, Or
from fmsd.expression.variables import BinaryVariable

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


def test_plain():
    lhs = And(Or(a, b), c)
    rhs = And(a, c)
    assert lhs.diff(rhs) == [0]
    assert rhs.diff(lhs) == [0]
    assert lhs.diff(lhs) is None


def test_recursive():
    lhs = And(And(a, b), c)
    rhs = And(And(a, Or(a, b)), And(b, c))
    assert lhs.diff(rhs) == [0, 1]
    assert rhs.diff(lhs) == [0, 1]


def test_start():
    lhs = And(And(a, b), c)
    rhs = And(And(a, Or(a, b)), And(b, c))
    assert lhs.diff(rhs, [0, 1]) == [1]
    assert rhs.diff(lhs, [0, 1]) == [1]
    assert lhs.diff(rhs, [1]) is None
    assert rhs.diff(lhs, [1]) is None
