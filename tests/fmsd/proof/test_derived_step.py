from fmsd.expression.operators.binary import And, Implies, Flip, Or
from fmsd.expression.variables import BinaryVariable
from fmsd.expression.constants import TRUE, FALSE
from fmsd.proof.derived_step import DerivedStepProof, DerivedChainProof
from fmsd.proof.step import StepProof, Step
from fmsd.rule.rules.binary import rule_commutative_and

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


def test_simple():
    proof = DerivedStepProof(
        And(a, b), And(b, a)
    )
    assert proof.verify()
    assert proof.hint == "commutative_and"


def test_invalid():
    proof = DerivedStepProof(
        And(a, b), And(b, c)
    )
    assert not proof.verify()


def test_deep():
    src = And(And(And(a, b), b), b)
    dst = And(And(And(b, a), b), b)
    proof = DerivedStepProof(
        src, dst
    )
    assert proof.verify()
    assert proof.hint == "commutative_and"
    assert proof.formalize() == StepProof(
        src, dst, [
            Step([0, 0], rule_commutative_and)
        ]
    )


def test_multiple():
    """
    Exercise 6m
    """
    src = Implies(Implies(a, Flip(a)), Flip(a))
    dst = TRUE
    proof = DerivedChainProof(
        src, dst, [
            src,
            Implies(Or(Flip(a), Flip(a)), Flip(a)),
            Implies(Flip(a), Flip(a)),
            dst
        ]
    )
    assert proof.verify()
    print(proof.formalize())
