import pytest

from fmsd.expression.variables import BinaryVariable, NumericVariable
from fmsd.expression.operators.binary import Flip, And
from fmsd.expression.operators.numeric import Negate, Plus

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")
x = NumericVariable("x")
y = NumericVariable("y")
z = NumericVariable("z")


def test_op1():
    Flip(a)
    with pytest.raises(AssertionError):
        Flip(a, b)
    with pytest.raises(AssertionError):
        Flip(x)
    Negate(x)
    with pytest.raises(AssertionError):
        Negate(x, y)
    with pytest.raises(AssertionError):
        Negate(a)