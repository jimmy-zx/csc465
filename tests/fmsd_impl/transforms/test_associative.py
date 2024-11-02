import pytest

import fmsd_impl.operators.binary as binop
import fmsd_impl.operators.generic as genop
import fmsd_impl.operators.numeric as numop
from fmsd.ast.node import Variable
from fmsd_impl.operators.props import Associative, Commutative
from fmsd_impl.transforms.prop import t_associative

a = Variable("a")
b = Variable("b")
c = Variable("c")
d = Variable("d")


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
    assert trf.verify(op(a, op(b, c)), op(op(a, b), c)) == issubclass(op, Associative)
    assert trf.verify(op(op(a, b), c), op(a, op(b, c))) == issubclass(op, Associative)
    assert trf.verify(op(a, op(b, op(c, d))), op(op(a, b), op(c, d))) == issubclass(
        op, Associative
    )
    assert trf.verify(op(a, op(b, op(c, d))), op(op(op(a, b), c), d)) == issubclass(
        op, Associative
    )
    assert trf.verify(op(a, op(b, op(c, d))), op(op(b, a), op(c, d))) == (
        issubclass(op, Associative) and issubclass(op, Commutative)
    )
    assert trf.verify(op(a, op(b, op(c, d))), op(op(op(b, a), c), d)) == (
        issubclass(op, Associative) and issubclass(op, Commutative)
    )
