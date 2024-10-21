import fmsd.utils.patch.binary
from fmsd.expression.operators.binary import And, Or
from fmsd.expression.variables import BinaryVariable
from fmsd.expression.variables import NumericVariable, NumericSingularVariable
from fmsd.utils import config

assert fmsd.utils.patch.binary


def test_singular():
    assert NumericVariable("a") != NumericSingularVariable("a")
    assert NumericSingularVariable("a") != NumericVariable("a")


def test_simple():
    a = BinaryVariable("a")
    b = BinaryVariable("b")
    c = BinaryVariable("c")
    config.TRACE = True
    d = Or(And(a, b), c)
    e = a & b
    assert d
    assert e
