from fmsd.ast.node import Node, VarNode
from fmsd_impl.operators import Context


def test_context():
    a = VarNode("a")
    b = VarNode("b")
    c = VarNode("c")
    tree = Node(a, Context(Node(b, Context(a, c)), b))
    assert tree.get([1, 0, 1, 0]).context() == [c, b]
