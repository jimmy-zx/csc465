import pytest

import fmsd.expression.operators.binary as binop
import fmsd.expression.operators.generic as genop
import fmsd.expression.operators.numeric as numop
import fmsd.utils.patch.binary
import fmsd.utils.patch.numeric
from fmsd.expression.operators import CommutativeOperator
from fmsd.expression.variables import BinaryVariable, NumericVariable
from fmsd.transform.transforms.prop import t_commutative

assert fmsd.utils.patch.binary
assert fmsd.utils.patch.numeric

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")

x = NumericVariable("x")
y = NumericVariable("y")
z = NumericVariable("z")


@pytest.mark.parametrize(
    "op",
    [
        binop.And,
        binop.Or,
        binop.Implies,
        binop.ImpliedBy,
        genop.Equals,
        genop.NotEquals,
    ],
)
def test_commutative_binary(op):
    trf = t_commutative
    assert trf.verify(op(a, b), op(b, a)) == issubclass(op, CommutativeOperator)


@pytest.mark.parametrize(
    "op",
    [
        numop.Plus,
        numop.Minus,
        numop.Multiply,
        numop.DividedBy,
        numop.Max,
        numop.Min,
        numop.LessThan,
        numop.LessThanOrEqualsTo,
        numop.GreaterThan,
        numop.GreaterThanOrEqualsTo,
        genop.Equals,
        genop.NotEquals,
    ],
)
def test_commutative_numeric(op):
    trf = t_commutative
    assert trf.verify(op(x, y), op(y, x)) == issubclass(op, CommutativeOperator)
