from fmsd.expression.constants import TRUE as T, FALSE as F
from fmsd.expression.operators.binary import *
from fmsd.expression.rules.binary import rule_excluded_middle, rule_noncontradiction, rule_base, rule_mirror, \
    rule_double_negation, rule_duality, rule_exclusion, rule_material_implication, rule_inclusion_and, rule_inclusion_or
from fmsd.expression.rules.table import rule_table
from fmsd.expression.variables import BinaryVariable

a = BinaryVariable("a")
b = BinaryVariable("b")
x = BinaryVariable("x")
y = BinaryVariable("y")
z = BinaryVariable("z")


def test_binary():
    assert T == T
    assert rule_table(Flip(F)) == T
    assert rule_table(NotEquals(T, F)) == T


def test_excluded_middle():
    assert rule_excluded_middle(Or(a, Flip(a))) == T
    assert rule_excluded_middle(T, a) == Or(a, Flip(a))


def test_noncontradiction():
    assert rule_noncontradiction(And(a, Flip(a))) == F
    assert rule_noncontradiction(F, a) == And(a, Flip(a))


def test_base():
    assert rule_base(And(a, F)) == F
    assert rule_base(Or(a, T)) == T
    assert rule_base(Implies(a, T)) == T
    assert rule_base(Implies(F, a)) == T


def test_mirror():
    assert rule_mirror(Implies(a, b)) == ImpliedBy(b, a)
    assert rule_mirror(ImpliedBy(a, b)) == Implies(b, a)


def test_double_negation():
    assert rule_double_negation(Flip(Flip(a))) == a
    assert rule_double_negation(a) == Flip(Flip(a))


def test_duality():
    assert rule_duality(Flip(And(a, b))) == Or(Flip(a), Flip(b))
    assert rule_duality(Flip(Or(a, b))) == And(Flip(a), Flip(b))


def test_exclusion():
    assert rule_exclusion(Implies(a, b)) == Implies(Flip(b), Flip(a))
    assert rule_exclusion(Equals(a, Flip(b))) == NotEquals(a, b)
    assert rule_exclusion(NotEquals(a, b)) == Equals(a, Flip(b))


def test_material_implication():
    assert rule_material_implication(Implies(a, b)) == Or(Flip(a), b)
    assert rule_material_implication(Or(a, b)) == Implies(Flip(a), b)


def test_inclusion():
    assert rule_inclusion_and(Implies(a, b)) == Equals(And(a, b), a)
    assert rule_inclusion_and(Equals(And(a, b), a)) == Implies(a, b)
    assert rule_inclusion_or(Implies(a, b)) == Equals(Or(a, b), b)
    assert rule_inclusion_or(Equals(Or(a, b), b)) == Implies(a, b)
