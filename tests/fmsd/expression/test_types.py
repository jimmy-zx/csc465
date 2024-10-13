import pytest

from fmsd.expression.operators.generic import Equals
from fmsd.expression.types import Type
from fmsd.expression.variables import NumericVariable, BinaryVariable


def test_equals():
    a = BinaryVariable("a")
    x = NumericVariable("x")
    with pytest.raises(AssertionError):
        Equals(a, x)
    assert Equals(a, a).type() == Type.BINARY
    assert Equals(x, x).type() == Type.BINARY
    assert Equals(Equals(a, a), Equals(x, x)).type() == Type.BINARY
