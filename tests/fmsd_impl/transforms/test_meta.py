from fmsd.ast import VarNode
from fmsd_impl.operators import Equals, VTCondition
from fmsd_impl.transforms.expr import ExpressionTransform


def test_vtcondition():
    a = VarNode("a")
    b = VarNode("b")
    c = VarNode("c")
    trf = ExpressionTransform(VTCondition(Equals(a, b), lambda vt: vt[a] == vt[b]))
    assert isinstance(trf.expr, VTCondition)
    assert not trf.verify(a, b)
    assert trf.verify(a, a)
    assert trf.verify(c, c)
    trf1 = ExpressionTransform(VTCondition(Equals(a, b), lambda vt: vt[a] == vt[b]))
    trf2 = ExpressionTransform(VTCondition(Equals(b, c), trf.expr.cond))
    trf3 = ExpressionTransform(VTCondition(Equals(a, b), trf.expr.cond))
    assert trf != trf1
    assert trf != trf2
    assert trf == trf3
