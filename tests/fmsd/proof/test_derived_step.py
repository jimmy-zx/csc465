import pytest

# noinspection PyUnresolvedReferences
import fmsd.utils.patch.binary
from fmsd.expression.constants.binary import TRUE
from fmsd.expression.operators.binary import Or, Equals
from fmsd.expression.variables import BinaryVariable
from fmsd.proof.derived_step import DerivedStepProof, DerivedChainProof, DerivedEquivChainProof
from fmsd.proof.step import StepProof, Step
from fmsd.rule.rules.binary import rule_commutative_and, rule_commutative_or
from fmsd.utils.patchops.infix import EQ, NEQ

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


def test_simple():
    proof = DerivedStepProof(
        a & b, b & a
    )
    assert proof.verify()
    assert proof.formalize() == StepProof(
        a & b, b & a, [
            Step([], rule_commutative_and, {"a": a, "b": b})
        ]
    )


def test_invalid():
    proof = DerivedStepProof(
        a & b, b & c
    )
    with pytest.raises(Exception) as ex:
        assert proof.verify()


def test_invalid_mult():
    proof = DerivedStepProof(
        (a | b) & (a | c), (b | a) & (c | a)
    )
    assert proof.verify()
    assert proof.formalize() == StepProof(
        (a | b) & (a | c), (b | a) & (c | a), [
            Step([0], rule_commutative_or, {"a": a, "b": b}),
            Step([1], rule_commutative_or, {"a": a, "b": c}),
        ]
    )


def test_deep():
    src = ((a & b) & b) & b
    dst = ((b & a) & b) & b
    proof = DerivedStepProof(
        src, dst
    )
    assert proof.verify()
    assert proof.formalize() == StepProof(
        src, dst, [
            Step([0, 0], rule_commutative_and, {"a": a, "b": b})
        ]
    )


def test_multiple():
    """
    Exercise 6m
    """
    src = (a >> ~a) >> ~a
    dst = TRUE
    proof = DerivedChainProof(
        src, dst, [
            src,
            (~a | ~a) >> ~a,
            ~a >> ~a,
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


def test_parallel():
    """
    Exercise 6s
    """
    src = ((a >> (a & b)) @ EQ @ (a >> b)) & ((a >> b) @ EQ @ ((a | b) >> b))
    dst = TRUE
    proof = DerivedEquivChainProof(src, dst, [
        ((a >> (a & b)) @ EQ @ (a >> b)) & ((a >> b) @ EQ @ ((a | b) >> b)),
        (((a >> a) & (a >> b)) @ EQ @ (a >> b)) & ((a >> b) @ EQ @ ((a >> b) & (b >> b))),
        ((TRUE & (a >> b)) @ EQ @ (a >> b)) & ((a >> b) @ EQ @ ((a >> b) & TRUE)),
        ((a >> b) @ EQ @ (a >> b)) & ((a >> b) @ EQ @ (a >> b)),
        TRUE & TRUE,
        TRUE
    ])
    assert proof.verify()
