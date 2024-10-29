from fmsd.ast.node import Variable
from fmsd.ast_ext.constant import Constant


def test_match():
    A = Constant("A")
    B = Constant("B")
    a = Variable("a")
    assert a.match(A, {}) == {"a": A}
    assert A.match(A, {}) == {}
    assert A.match(a, {}) is None
    assert A.match(B, {}) is None
