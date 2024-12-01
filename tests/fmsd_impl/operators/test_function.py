import pytest

from fmsd.ast import VarNode
from fmsd.ast_ext import Variable
from fmsd.impl.constants import TRUE
from fmsd_impl.constants import NAT
from fmsd_impl.operators import Function, FunctionCompose


def test_func_vars():
    x = Variable("x")
    y = VarNode("y")
    D = VarNode("D")
    f1 = Function(x, D, x)
    assert f1.sym_decls() == {x}
    f2 = Function(y, D, FunctionCompose(f1, y))
    assert f2.sym_decls() == {x, y}
    assert f2.nodes[2].sym_decls() == {x}


def test_func_init():
    x = Variable("x")
    with pytest.raises(AssertionError):
        Function(x, x, TRUE)
    with pytest.raises(AssertionError):
        Function(x, NAT, FunctionCompose(x, NAT, x))
    Function(x, NAT, x)
