import pytest

import fmsd_impl.patch.binary
import fmsd_impl.operators.binary as binop
import fmsd_impl.operators.generic as genop
from fmsd.ast.node import Variable
from fmsd.ast_ext.operator import Commutative
from fmsd_impl.transforms.prop import t_commutative
import fmsd_impl.operators.numeric as numop

assert fmsd_impl.patch.binary

a = Variable("a")
b = Variable("b")


@pytest.mark.parametrize(
    "op",
    [
        binop.And,
        binop.Or,
        binop.Implies,
        binop.ImpliedBy,
        genop.Equals,
        genop.NotEquals,
        numop.Plus,
        numop.Minus,
        numop.Multiply,
        numop.DividedBy,
        numop.Power,
        numop.Max,
        numop.Min,
        numop.LessThan,
        numop.LessThanOrEqualsTo,
        numop.GreaterThan,
        numop.GreaterThanOrEqualsTo,
    ],
)
def test_commutative(op):
    trf = t_commutative
    assert trf.verify(op(a, b), op(b, a)) == issubclass(op, Commutative)

