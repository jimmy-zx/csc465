import fmsd.utils.patch.binary
from fmsd.expression.variables import BinaryVariable

assert fmsd.utils.patch.binary

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


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
