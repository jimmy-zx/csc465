import pytest

import fmsd_impl.patch.binary
import fmsd_impl.operators.binary as binop
import fmsd_impl.operators.generic as genop
from fmsd.ast.node import Variable
from fmsd.ast_ext.operator import Commutative
from fmsd_impl.transforms.prop import t_commutative

assert fmsd_impl.patch.binary

a = Variable("a")
b = Variable("b")
c = Variable("c")

x = Variable("x")
y = Variable("y")
z = Variable("z")


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
    assert trf.verify(op(a, b), op(b, a)) == issubclass(op, Commutative)


@pytest.mark.parametrize(
    "op",
    [
        genop.Equals,
        genop.NotEquals,
    ],
)
def test_commutative_numeric(op):
    trf = t_commutative
    assert trf.verify(op(x, y), op(y, x)) == issubclass(op, Commutative)
