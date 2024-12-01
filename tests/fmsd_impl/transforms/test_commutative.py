import pytest

import fmsd_impl.operators.binary as binop
import fmsd_impl.operators.generic as genop
import fmsd_impl.operators.numeric as numop
import fmsd_impl.patch.binary
from fmsd.ast.node import VarNode
from fmsd_impl.operators.props import Commutative
from fmsd_impl.transforms.prop import t_commutative

assert fmsd_impl.patch.binary

a = VarNode("a")
b = VarNode("b")


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
    assert trf.verify(op(a, b), op(b, a)) == Commutative.has_prop(op)
