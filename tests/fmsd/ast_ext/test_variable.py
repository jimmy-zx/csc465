from fmsd.ast import Node, VarNode
from fmsd.ast_ext import Variable


def test_variable():
    a1 = VarNode("a")
    a2 = Variable("a")
    b1 = VarNode("b")
    b2 = Variable("b")
    assert a1 != a2
    assert hash(a1) != hash(a2)
    assert Node(a1, a2, b1, b2).eval(
        {
            a1: b1,
            a2: b2,
            b1: a2,
            b2: a1,
        }
    ) == Node(b1, b2, a2, a1)
    assert Node(a1, a2, b1, b2).match(Node(a2, a2, b2, b2), {}) == {a1: a2, b1: b2}
    assert Node(a1, a2, b1, b2).match(Node(a1, a1, b1, b1), {}) is None
