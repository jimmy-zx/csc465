import pytest

from fmsd.ast.node import VarNode
from fmsd_impl.operators.binary import Flip

a = VarNode("a")
b = VarNode("b")


def test_op1():
    Flip(a)
    with pytest.raises(AssertionError):
        Flip(a, b)
