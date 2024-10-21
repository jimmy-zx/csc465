from fmsd.expression.constants.binary import TRUE as T, FALSE as F
from fmsd.expression.operators.binary import And, Or, Implies, ImpliedBy, Flip
from fmsd.expression.operators.generic import Equals, NotEquals
from fmsd.expression.variables import BinaryVariable
from fmsd.rule.rules.binary import (
    rule_excluded_middle,
    rule_noncontradiction,
    rule_base_and,
    rule_base_or,
    rule_mirror,
    rule_double_negation,
    rule_duality_and,
    rule_duality_or,
    rule_exclusion,
    rule_material_implication,
    rule_inclusion_and,
    rule_inclusion_or,
    rule_base_implies_true,
    rule_base_implies_false,
    rule_contrapositive,
)
from fmsd.transform.expr import ExpressionTransform
from fmsd.transform.transforms.binary_table import func_rule_table

a = BinaryVariable("a")
b = BinaryVariable("b")
x = BinaryVariable("x")
y = BinaryVariable("y")
z = BinaryVariable("z")


def test_binary():
    assert T == T
    assert func_rule_table(Flip(F)) == T
    assert func_rule_table(NotEquals(T, F)) == T


def test_excluded_middle():
    assert ExpressionTransform(rule_excluded_middle).verify(Or(a, Flip(a)), T)
    assert ExpressionTransform(rule_excluded_middle).verify(T, Or(a, Flip(a)))


def test_noncontradiction():
    assert ExpressionTransform(rule_noncontradiction).verify(And(a, Flip(a)), F)
    assert ExpressionTransform(rule_noncontradiction).verify(F, And(a, Flip(a)))


def test_base():
    assert ExpressionTransform(rule_base_and).verify(And(a, F), F)
    assert ExpressionTransform(rule_base_or).verify(Or(a, T), T)
    assert ExpressionTransform(rule_base_implies_true).verify(Implies(a, T), T)
    assert ExpressionTransform(rule_base_implies_false).verify(Implies(F, a), T)


def test_mirror():
    assert ExpressionTransform(rule_mirror).verify(Implies(a, b), ImpliedBy(b, a))
    assert ExpressionTransform(rule_mirror).verify(ImpliedBy(a, b), Implies(b, a))


def test_double_negation():
    assert ExpressionTransform(rule_double_negation).verify(Flip(Flip(a)), a)
    assert ExpressionTransform(rule_double_negation).verify(a, Flip(Flip(a)))


def test_duality():
    assert ExpressionTransform(rule_duality_and).verify(
        Flip(And(a, b)), Or(Flip(a), Flip(b))
    )
    assert ExpressionTransform(rule_duality_or).verify(
        Flip(Or(a, b)), And(Flip(a), Flip(b))
    )


def test_exclusion():
    assert ExpressionTransform(rule_contrapositive).verify(
        Implies(a, b), Implies(Flip(b), Flip(a))
    )
    assert ExpressionTransform(rule_exclusion).verify(
        Equals(a, Flip(b)), NotEquals(a, b)
    )
    assert ExpressionTransform(rule_exclusion).verify(
        NotEquals(a, b), Equals(a, Flip(b))
    )


def test_material_implication():
    assert ExpressionTransform(rule_material_implication).verify(
        Implies(a, b), Or(Flip(a), b)
    )
    assert ExpressionTransform(rule_material_implication).verify(
        Or(Flip(a), b), Implies(a, b)
    )


def test_inclusion():
    assert ExpressionTransform(rule_inclusion_and).verify(
        Implies(a, b), Equals(And(a, b), a)
    )
    assert ExpressionTransform(rule_inclusion_and).verify(
        Equals(And(a, b), a), Implies(a, b)
    )
    assert ExpressionTransform(rule_inclusion_or).verify(
        Implies(a, b), Equals(Or(a, b), b)
    )
    assert ExpressionTransform(rule_inclusion_or).verify(
        Equals(Or(a, b), b), Implies(a, b)
    )
