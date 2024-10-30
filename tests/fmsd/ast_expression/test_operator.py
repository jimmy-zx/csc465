import pytest

from fmsd.ast.node import Variable
from fmsd.ast_ext.operator import Operator


def test_init():
    a = Variable("a")
    b = Variable("b")

    class Op2(Operator):
        N = 2

    Op2(a, b)

    with pytest.raises(AssertionError):
        Op2(a)

    with pytest.raises(AssertionError):
        Op2(a, b, b)
