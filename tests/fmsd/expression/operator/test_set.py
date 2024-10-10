from fmsd.expression.operators.binary import And, Or
from fmsd.expression.variables import BinaryVariable

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


def test_get():
    tree = And(Or(a, b), c)
    assert tree.get([0]) == Or(a, b)
    assert tree.get([1]) == c
    assert tree.get([0, 0]) == a
    assert tree.get([0, 1]) == b


def test_set():
    tree = And(Or(a, b), c)
    tree.set([0, 0], b)
    assert tree == And(Or(b, b), c)