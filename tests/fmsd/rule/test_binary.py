from fmsd.ast.node import Variable
from fmsd_impl.transforms.expr import ExpressionTransform
from fmsd_impl.transforms.axioms.binary import (
    axiom_excluded_middle,
    axiom_noncontradiction,
    axiom_base_and,
    axiom_base_or,
    axiom_mirror,
    axiom_double_negation,
    axiom_duality_and,
    axiom_duality_or,
    axiom_exclusion,
    axiom_material_implication,
    axiom_inclusion_and,
    axiom_inclusion_or,
    axiom_base_implies_true,
    axiom_base_implies_false,
    axiom_contrapositive,
)
from fmsd_impl.constants.basic import TRUE as T, FALSE as F
from fmsd_impl.operators.binary import And, Or, Implies, ImpliedBy, Flip
from fmsd_impl.operators.generic import Equals, NotEquals

a = Variable("a")
b = Variable("b")
x = Variable("x")
y = Variable("y")
z = Variable("z")


# def test_binary():
#     assert T == T
#     assert func_rule_table(Flip(F)) == T
#     assert func_rule_table(NotEquals(T, F)) == T


def test_excluded_middle():
    assert ExpressionTransform(axiom_excluded_middle).verify(Or(a, Flip(a)), T)
    assert ExpressionTransform(axiom_excluded_middle).verify(T, Or(a, Flip(a)))


def test_noncontradiction():
    assert ExpressionTransform(axiom_noncontradiction).verify(And(a, Flip(a)), F)
    assert ExpressionTransform(axiom_noncontradiction).verify(F, And(a, Flip(a)))


def test_base():
    assert ExpressionTransform(axiom_base_and).verify(And(a, F), F)
    assert ExpressionTransform(axiom_base_or).verify(Or(a, T), T)
    assert ExpressionTransform(axiom_base_implies_true).verify(Implies(a, T), T)
    assert ExpressionTransform(axiom_base_implies_false).verify(Implies(F, a), T)


def test_mirror():
    assert ExpressionTransform(axiom_mirror).verify(Implies(a, b), ImpliedBy(b, a))
    assert ExpressionTransform(axiom_mirror).verify(ImpliedBy(a, b), Implies(b, a))


def test_double_negation():
    assert ExpressionTransform(axiom_double_negation).verify(Flip(Flip(a)), a)
    assert ExpressionTransform(axiom_double_negation).verify(a, Flip(Flip(a)))


def test_duality():
    assert ExpressionTransform(axiom_duality_and).verify(
        Flip(And(a, b)), Or(Flip(a), Flip(b))
    )
    assert ExpressionTransform(axiom_duality_or).verify(
        Flip(Or(a, b)), And(Flip(a), Flip(b))
    )


def test_exclusion():
    assert ExpressionTransform(axiom_contrapositive).verify(
        Implies(a, b), Implies(Flip(b), Flip(a))
    )
    assert ExpressionTransform(axiom_exclusion).verify(
        Equals(a, Flip(b)), NotEquals(a, b)
    )
    assert ExpressionTransform(axiom_exclusion).verify(
        NotEquals(a, b), Equals(a, Flip(b))
    )


def test_material_implication():
    assert ExpressionTransform(axiom_material_implication).verify(
        Implies(a, b), Or(Flip(a), b)
    )
    assert ExpressionTransform(axiom_material_implication).verify(
        Or(Flip(a), b), Implies(a, b)
    )


def test_inclusion():
    assert ExpressionTransform(axiom_inclusion_and).verify(
        Implies(a, b), Equals(And(a, b), a)
    )
    assert ExpressionTransform(axiom_inclusion_and).verify(
        Equals(And(a, b), a), Implies(a, b)
    )
    assert ExpressionTransform(axiom_inclusion_or).verify(
        Implies(a, b), Equals(Or(a, b), b)
    )
    assert ExpressionTransform(axiom_inclusion_or).verify(
        Equals(Or(a, b), b), Implies(a, b)
    )
