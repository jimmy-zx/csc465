from fmsd.ast import VarNode
from fmsd.ast_ext import Variable
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
