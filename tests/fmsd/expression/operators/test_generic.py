from fmsd.expression.constants import TRUE as T, FALSE as F
from fmsd.expression.operators.binary import *
from fmsd.expression.variables import BinaryVariable
# noinspection PyUnresolvedReferences
import fmsd.expression.patch.expression


def test_reflexivity():
    assert Equals(BinaryVariable("x"), BinaryVariable("x")).rule_reflexivity() == T

def test_symmetry():
    x = BinaryVariable("x")
    y = BinaryVariable("y")
    assert Equals(x, y).rule_symmetry() == Equals(y, x)

def test_transitivity():
    x = BinaryVariable("x")
    y = BinaryVariable("y")
    z = BinaryVariable("z")
    assert And(Equals(x, y), Equals(y, z)).rule_transitivity() == Equals(x, z)


def test_unequality():
    x = BinaryVariable("x")
    y = BinaryVariable("y")
    assert NotEquals(x, y).rule_unequality() == Flip(Equals(x, y))
    assert Flip(Equals(x, y)).rule_unequality() == NotEquals(x, y)


def test_case_base():
    a = BinaryVariable("x")
    x = BinaryVariable("x")
    y = BinaryVariable("y")
    assert Ternary(T, x, y).rule_case_base() == x
    assert Ternary(F, x, y).rule_case_base() == y
    assert Ternary(a, x, x).rule_case_idempotent() == x
    assert Ternary(a, x, y).rule_case_reversal() == Ternary(Flip(a), y, x)
