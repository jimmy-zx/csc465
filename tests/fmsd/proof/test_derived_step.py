import pytest

from fmsd.expression.operators.binary import And, Implies, Flip, Or, Equals
from fmsd.expression.variables import BinaryVariable
from fmsd.expression.constants import TRUE, FALSE
from fmsd.proof.derived_step import DerivedStepProof, DerivedChainProof, DerivedEquivChainProof
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
    with pytest.raises(Exception) as ex:
        proof.verify()


def test_invalid_mult():
    proof = DerivedStepProof(
        And(Or(a, b), Or(a, c)), And(Or(b, a), Or(c, a))
    )
    with pytest.raises(Exception) as ex:
        proof.verify()


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
            Step([0, 0], rule_commutative_and, {"a": a, "b": b})
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


def test_multiple_equiv():
    """
    Exercise 6p
    """
    src = Or(Equals(a, b), Or(Equals(a, c), Equals(b, c)))
    dst = TRUE
    proof = DerivedEquivChainProof(
        src, dst, [
            src,
            Or(Equals(a, b), Or(Equals(a, c), Equals(b, Equals(TRUE, c)))),
            Or(Equals(a, b), Or(Equals(a, c), Equals(b, Equals(c, TRUE)))),
            Or(Equals(a, b), Or(Equals(a, c), Equals(b, Equals(TRUE, c)))),
            Or(Equals(a, b), Or(Equals(a, c), Equals(b, Equals(Equals(a, a), c)))),
            Or(Equals(a, b), Or(Equals(a, c), Equals(b, Equals(a, Equals(a, c))))),
            Or(Equals(a, b), Or(Equals(a, c), Equals(Equals(b, a), Equals(a, c)))),
            Or(Or(Equals(a, b), Equals(a, c)), Equals(Equals(b, a), Equals(a, c))),
            Equals(Or(Or(Equals(a, b), Equals(a, c)), Equals(b, a)), Or(Or(Equals(a, b), Equals(a, c)), Equals(a, c))),
            Equals(Or(Or(Equals(a, b), Equals(a, c)), Equals(a, b)), Or(Or(Equals(a, b), Equals(a, c)), Equals(a, c))),
            Equals(Or(Or(Equals(a, c), Equals(a, b)), Equals(a, b)), Or(Or(Equals(a, b), Equals(a, c)), Equals(a, c))),
            Equals(Or(Equals(a, c), Or(Equals(a, b), Equals(a, b))), Or(Or(Equals(a, b), Equals(a, c)), Equals(a, c))),
            Equals(Or(Equals(a, c), Or(Equals(a, b), Equals(a, b))), Or(Equals(a, b), Or(Equals(a, c), Equals(a, c)))),
            Equals(Or(Equals(a, c), Equals(a, b)), Or(Equals(a, b), Or(Equals(a, c), Equals(a, c)))),
            Equals(Or(Equals(a, c), Equals(a, b)), Or(Equals(a, b), Equals(a, c))),
            Equals(Or(Equals(a, b), Equals(a, c)), Or(Equals(a, b), Equals(a, c))),
            dst
        ]
    )
    assert proof.verify()
    print(proof.formalize())
