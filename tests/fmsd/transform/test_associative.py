import pytest

import fmsd.expression.operators.binary as binop
import fmsd.expression.operators.generic as genop
import fmsd.expression.operators.numeric as numop
import fmsd.utils.patch.binary
import fmsd.utils.patch.numeric
from fmsd.expression.operators import AssociativeOperator, CommutativeOperator
from fmsd.expression.variables import BinaryVariable, NumericVariable
from fmsd.transform.transforms.prop import t_associative

assert fmsd.utils.patch.binary
assert fmsd.utils.patch.numeric

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")
d = BinaryVariable("d")

w = NumericVariable("w")
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
    trf = t_associative
    assert trf.verify(op(a, op(b, c)), op(op(a, b), c)) == issubclass(
        op, AssociativeOperator
    )
    assert trf.verify(op(op(a, b), c), op(a, op(b, c))) == issubclass(
        op, AssociativeOperator
    )
    assert trf.verify(op(a, op(b, op(c, d))), op(op(a, b), op(c, d))) == issubclass(
        op, AssociativeOperator
    )
    assert trf.verify(op(a, op(b, op(c, d))), op(op(op(a, b), c), d)) == issubclass(
        op, AssociativeOperator
    )
    assert trf.verify(op(a, op(b, op(c, d))), op(op(b, a), op(c, d))) == (
        issubclass(op, AssociativeOperator) and issubclass(op, CommutativeOperator)
    )
    assert trf.verify(op(a, op(b, op(c, d))), op(op(op(b, a), c), d)) == (
        issubclass(op, AssociativeOperator) and issubclass(op, CommutativeOperator)
    )


@pytest.mark.parametrize(
    "op",
    [
        numop.Plus,
        numop.Minus,
        numop.Multiply,
        numop.DividedBy,
        numop.Max,
        numop.Min,
    ],
)
def test_commutative_numeric(op):
    trf = t_associative
    assert trf.verify(op(x, op(y, z)), op(op(x, y), z)) == issubclass(
        op, AssociativeOperator
    )
    assert trf.verify(op(op(x, y), z), op(x, op(y, z))) == issubclass(
        op, AssociativeOperator
    )
    assert trf.verify(op(w, op(x, op(y, z))), op(op(w, x), op(y, z))) == issubclass(
        op, AssociativeOperator
    )
    assert trf.verify(op(w, op(x, op(y, z))), op(op(op(w, x), y), z)) == issubclass(
        op, AssociativeOperator
    )
    assert trf.verify(op(w, op(x, op(y, z))), op(op(x, w), op(y, z))) == (
        issubclass(op, AssociativeOperator) and issubclass(op, CommutativeOperator)
    )
    assert trf.verify(op(w, op(x, op(y, z))), op(op(op(x, w), y), z)) == (
        issubclass(op, AssociativeOperator) and issubclass(op, CommutativeOperator)
    )
