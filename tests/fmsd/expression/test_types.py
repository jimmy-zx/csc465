from fmsd.expression.constants.binary import FALSE
from fmsd.expression.constants.numeric import ZERO
from fmsd.expression.operators.generic import Equals
from fmsd.expression.operators.set_ import Set
from fmsd.expression.types import Type
from fmsd.expression.variables import (
    NumericVariable,
    BinaryVariable,
    SetVariable,
    AnyVariable,
)


def test_equals():
    a = BinaryVariable("a")
    x = NumericVariable("x")
    assert Equals(a, a).type() == Type.BINARY
    assert Equals(x, x).type() == Type.BINARY
    assert Equals(Equals(a, a), Equals(x, x)).type() == Type.BINARY


def test_match():
    for lhs in Type:
        assert lhs.match(lhs)
        assert Type.ANY.match(lhs)
    assert not Type.NUMERIC.match(Type.ANY)
    assert not Type.SET.match(Type.BINARY)


def test_vmatch():
    assert BinaryVariable("x").vmatch(FALSE, {})
    assert NumericVariable("a").vmatch(ZERO, {})
    assert SetVariable("S", Type.NUMERIC).vmatch(Set(ZERO), {})

    assert AnyVariable("a").vmatch(FALSE, {})
    assert SetVariable("S", Type.ANY).vmatch(Set(FALSE), {})

    assert SetVariable("S", Type.BINARY).vmatch(Set(ZERO), {}) is None
    assert SetVariable("S", Type.NUMERIC).vmatch(FALSE, {}) is None
    assert NumericVariable("a").vmatch(FALSE, {}) is None
