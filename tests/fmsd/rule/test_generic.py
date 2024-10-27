from fmsd.ast.node import Variable
from fmsd_impl.transforms.expr import ExpressionTransform
from fmsd_impl.axioms.binary_generic import (
    axiom_reflexivity,
    axiom_symmetry,
    axiom_transitivity,
    axiom_unequality,
    axiom_case_idempotent,
    axiom_case_reversal,
    axiom_case_base_true,
    axiom_case_base_false,
)
from fmsd_impl.constants.basic import TRUE as T, FALSE as F
from fmsd_impl.operators.binary import And, Flip
from fmsd_impl.operators.generic import Equals, NotEquals, Ternary

a = Variable("a")
x = Variable("x")
y = Variable("y")
z = Variable("z")


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
