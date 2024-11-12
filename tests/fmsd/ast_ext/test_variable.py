from fmsd.ast import Node, VarNode
from fmsd.ast_ext import Constant, Variable


def test_variable():
    """
    Matchable: (a=a) can match (b=b)
    Evaluatable: (a=a) {a:1} can be evaluated to {1=1}
    | Type     | Matchable | Evaluatable |
    |----------|-----------|-------------|
    | VarNode  | Yes       | Yes         |
    | Variable | No        | Yes         |
    | Constant | No        | No          |
    """
    a1 = VarNode("a")
    a2 = Variable("a")
    a3 = Constant("a")
    b1 = VarNode("b")
    b2 = Variable("b")
    b3 = Constant("b")
    assert a1 != a2
    assert a2 != a3
    assert a1 != a3
    assert hash(a1) != hash(a2)
    assert hash(a2) != hash(a3)
    assert hash(a1) != hash(a3)
    assert Node(a1, a2, a3, b1, b2, b3).eval(
        {
            a1: b1,
            a2: b2,
            a3: b3,
            b1: a2,
            b2: a1,
            b3: a3,
        }
    ) == Node(b1, b2, a3, a2, a1, b3)
    assert Node(a1, a2, b1, b2).match(Node(a2, a2, b2, b2), {}) == {a1: a2, b1: b2}
    assert Node(a1, a2, b1, b2).match(Node(a1, a1, b1, b1), {}) is None
    assert Node(a1, a3, b1, b3).match(Node(a3, a3, b3, b3), {}) == {a1: a3, b1: b3}
    assert Node(a1, a3, b1, b3).match(Node(a1, a1, b1, b1), {}) is None
