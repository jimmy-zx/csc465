from fmsd.ast.node import VarNode
from fmsd_impl.constants.basic import FALSE as F
from fmsd_impl.constants.basic import TRUE as T
from fmsd_impl.operators.binary import And, Flip
from fmsd_impl.operators.generic import Equals, NotEquals, Ternary
from fmsd_impl.transforms.axioms.generic import (
    axiom_case_base_false,
    axiom_case_base_true,
    axiom_case_idempotent,
    axiom_case_reversal,
    axiom_reflexivity,
    axiom_symmetry,
    axiom_transitivity,
    axiom_unequality,
)
from fmsd_impl.transforms.expr import ExpressionTransform

a = VarNode("a")
x = VarNode("x")
y = VarNode("y")
z = VarNode("z")


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
