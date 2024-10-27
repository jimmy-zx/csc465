import fmsd.utils.patch.binary
from fmsd.ast.node import Variable

assert fmsd.utils.patch.binary

a = Variable("a")
b = Variable("b")
c = Variable("c")


def test_get():
    tree = (a | b) & c
    assert tree.get([0]) == a | b
    assert tree.get([1]) == c
    assert tree.get([0, 0]) == a
    assert tree.get([0, 1]) == b


def test_set():
    tree = (a | b) & c
    tree.set([0, 0], b)
    assert tree == (b | b) & c
