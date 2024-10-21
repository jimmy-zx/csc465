from fmsd.expression.constants.binary import TRUE as T, FALSE as F
from fmsd.expression.operators.binary import And, Flip
from fmsd.expression.operators.generic import Equals, NotEquals, Ternary
from fmsd.expression.variables import BinaryVariable
from fmsd.rule.rules.binary.generic import (
    rule_reflexivity,
    rule_symmetry,
    rule_transitivity,
    rule_unequality,
    rule_case_idempotent,
    rule_case_reversal,
    rule_case_base_true,
    rule_case_base_false,
)
from fmsd.transform.expr import ExpressionTransform

a = BinaryVariable("a")
x = BinaryVariable("x")
y = BinaryVariable("y")
z = BinaryVariable("z")


def test_reflexivity():
    assert ExpressionTransform(rule_reflexivity).verify(Equals(x, x), T)
    assert ExpressionTransform(rule_reflexivity).verify(T, Equals(x, x))


def test_symmetry():
    assert ExpressionTransform(rule_symmetry).verify(Equals(x, y), Equals(y, x))
    assert ExpressionTransform(rule_symmetry).verify(Equals(y, x), Equals(x, y))


def test_transitivity():
    assert ExpressionTransform(rule_transitivity).verify(
        And(Equals(x, y), Equals(y, z)), Equals(x, z)
    )


def test_unequality():
    assert ExpressionTransform(rule_unequality).verify(
        NotEquals(x, y), Flip(Equals(x, y))
    )
    assert ExpressionTransform(rule_unequality).verify(
        Flip(Equals(x, y)), NotEquals(x, y)
    )


def test_case_base():
    assert ExpressionTransform(rule_case_base_true).verify(Ternary(T, x, y), x)
    assert ExpressionTransform(rule_case_base_false).verify(Ternary(F, x, y), y)


def test_case_idopotent():
    assert ExpressionTransform(rule_case_idempotent).verify(Ternary(a, x, x), x)


def test_case_reversal():
    assert ExpressionTransform(rule_case_reversal).verify(
        Ternary(a, x, y), Ternary(Flip(a), y, x)
    )
