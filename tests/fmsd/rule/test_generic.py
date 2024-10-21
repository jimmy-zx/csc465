from fmsd.expression.constants.binary import TRUE as T, FALSE as F
from fmsd.expression.operators.binary import And, Flip
from fmsd.expression.operators.generic import Equals, NotEquals, Ternary
from fmsd.expression.variables import BinaryVariable
from fmsd.transform.transforms.axioms.binary_generic import (
    axiom_reflexivity,
    axiom_symmetry,
    axiom_transitivity,
    axiom_unequality,
    axiom_case_idempotent,
    axiom_case_reversal,
    axiom_case_base_true,
    axiom_case_base_false,
)
from fmsd.transform.expr import ExpressionTransform

a = BinaryVariable("a")
x = BinaryVariable("x")
y = BinaryVariable("y")
z = BinaryVariable("z")


def test_reflexivity():
    assert ExpressionTransform(axiom_reflexivity).verify(Equals(x, x), T)
    assert ExpressionTransform(axiom_reflexivity).verify(T, Equals(x, x))


def test_symmetry():
    assert ExpressionTransform(axiom_symmetry).verify(Equals(x, y), Equals(y, x))
    assert ExpressionTransform(axiom_symmetry).verify(Equals(y, x), Equals(x, y))


def test_transitivity():
    assert ExpressionTransform(axiom_transitivity).verify(
        And(Equals(x, y), Equals(y, z)), Equals(x, z)
    )


def test_unequality():
    assert ExpressionTransform(axiom_unequality).verify(
        NotEquals(x, y), Flip(Equals(x, y))
    )
    assert ExpressionTransform(axiom_unequality).verify(
        Flip(Equals(x, y)), NotEquals(x, y)
    )


def test_case_base():
    assert ExpressionTransform(axiom_case_base_true).verify(Ternary(T, x, y), x)
    assert ExpressionTransform(axiom_case_base_false).verify(Ternary(F, x, y), y)


def test_case_idopotent():
    assert ExpressionTransform(axiom_case_idempotent).verify(Ternary(a, x, x), x)


def test_case_reversal():
    assert ExpressionTransform(axiom_case_reversal).verify(
        Ternary(a, x, y), Ternary(Flip(a), y, x)
    )
