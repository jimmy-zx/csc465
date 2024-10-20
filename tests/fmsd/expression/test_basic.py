from fmsd.expression.variables import NumericVariable, NumericSingularVariable
from fmsd.expression.operators.binary import And, Or
from fmsd.expression.variables import BinaryVariable
# noinspection PyUnresolvedReferences
import fmsd.utils.patch.binary
import fmsd.utils.config as config


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
