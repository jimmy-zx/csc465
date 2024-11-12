import pytest

from fmsd.ast.node import VarNode
from fmsd.ast_ext.operator import Operator


def test_init():
    a = VarNode("a")
    b = VarNode("b")

    class Op2(Operator):
        N = 2

    Op2(a, b)

    with pytest.raises(AssertionError):
        Op2(a)

    with pytest.raises(AssertionError):
        Op2(a, b, b)
