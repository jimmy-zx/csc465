import pytest

import fmsd_impl.operators.binary as binop
import fmsd_impl.operators.generic as genop
import fmsd_impl.operators.numeric as numop
from fmsd.ast.node import VarNode
from fmsd_impl.operators.props import Associative, Commutative
from fmsd_impl.transforms.prop import t_associative

a = VarNode("a")
b = VarNode("b")
c = VarNode("c")
d = VarNode("d")


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
def test_associative(op):
    trf = t_associative
    assert trf.verify(op(a, op(b, c)), op(op(a, b), c)) == Associative.has_prop(op)
    assert trf.verify(op(op(a, b), c), op(a, op(b, c))) == Associative.has_prop(op)
    assert trf.verify(
        op(a, op(b, op(c, d))), op(op(a, b), op(c, d))
    ) == Associative.has_prop(op)
    assert trf.verify(
        op(a, op(b, op(c, d))), op(op(op(a, b), c), d)
    ) == Associative.has_prop(op)
    assert trf.verify(op(a, op(b, op(c, d))), op(op(b, a), op(c, d))) == (
        Associative.has_prop(op) and Commutative.has_prop(op)
    )
    assert trf.verify(op(a, op(b, op(c, d))), op(op(op(b, a), c), d)) == (
        Associative.has_prop(op) and Commutative.has_prop(op)
    )
