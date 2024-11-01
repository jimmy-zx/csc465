from fmsd.ast.node import Node, Variable
from fmsd_impl.operators.context import Context


def test_context():
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")
    tree = Node(a, Context(Node(b, Context(a, c)), b))
    assert tree.get([1, 0, 1, 0]).context() == [c, b]
