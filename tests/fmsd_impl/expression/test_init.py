import pytest

from fmsd.ast.node import Variable
from fmsd_impl.operators.binary import Flip

a = Variable("a")
b = Variable("b")


def test_op1():
    Flip(a)
    with pytest.raises(AssertionError):
        Flip(a, b)
