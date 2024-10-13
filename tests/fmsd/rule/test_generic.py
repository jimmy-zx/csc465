from fmsd.expression.constants.binary import TRUE as T, FALSE as F
from fmsd.expression.operators.binary import *
from fmsd.expression.operators.generic import Equals, NotEquals, Ternary
from fmsd.rule.rules.binary.generic import rule_reflexivity, rule_symmetry, rule_transitivity, rule_unequality, \
    rule_case_idempotent, rule_case_reversal, rule_case_base_true, rule_case_base_false
from fmsd.expression.variables import BinaryVariable

a = BinaryVariable("a")
x = BinaryVariable("x")
y = BinaryVariable("y")
z = BinaryVariable("z")


def test_reflexivity():
    assert rule_reflexivity(Equals(x, x)) == T
    assert rule_reflexivity(T, {"x": x}) == Equals(x, x)


def test_symmetry():
    assert rule_symmetry(Equals(x, y)) == Equals(y, x)
    assert rule_symmetry(Equals(y, x)) == Equals(x, y)


def test_transitivity():
    assert rule_transitivity(And(Equals(x, y), Equals(y, z))) == Equals(x, z)


def test_unequality():
    assert rule_unequality(NotEquals(x, y)) == Flip(Equals(x, y))
    assert rule_unequality(Flip(Equals(x, y))) == NotEquals(x, y)


def test_case_base():
    assert rule_case_base_true(Ternary(T, x, y)) == x
    assert rule_case_base_false(Ternary(F, x, y)) == y


def test_case_idopotent():
    assert rule_case_idempotent(Ternary(a, x, x)) == x


def test_case_reversal():
    assert rule_case_reversal(Ternary(a, x, y)) == Ternary(Flip(a), y, x)
