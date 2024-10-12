from fmsd.expression.constants.binary import TRUE
from fmsd.expression.operators.binary import Equals, Implies, And, Flip
from fmsd.expression.variables import BinaryVariable
from fmsd.proof.step import Step, StepProof
from fmsd.rule.rules.binary import rule_conflation_and, rule_specialization, rule_portation, rule_noncontradiction, \
    rule_base_implies_false, rule_commutative_and
from fmsd.rule.rules.generic import rule_symmetry

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


def test_child():
    """
    Exercise 6e
    """
    orig = Equals(Equals(a, Implies(a, b)), And(a, b))
    assert Step([0], rule_symmetry).apply(orig) == Equals(Equals(Implies(a, b), a), And(a, b))


def test_root():
    """
    Exercise 6f
    """
    orig = And(Implies(a, c), Implies(b, Flip(c)))
    assert Step([], rule_conflation_and).apply(orig) == Implies(And(a, b), And(c, Flip(c)))


def test_single_step_proof():
    """
    Exercise 6g
    """
    src = And(a, Flip(b))
    dst = a
    steps = [Step([], rule_specialization)]
    proof = StepProof(src, dst, steps)
    assert proof.verify()


def test_multi_step_proof():
    """
    Exercise 6c
    """
    src = Implies(Flip(a), Implies(a, b))
    dst = TRUE
    steps = [
        Step([], rule_portation),
        Step([0], rule_commutative_and),
        Step([0], rule_noncontradiction),
        Step([], rule_base_implies_false),
    ]
    proof = StepProof(src, dst, steps)
    assert proof.verify()


def test_multi_step_proof_rev():
    """
    Exercise 6c
    """
    src = TRUE
    dst = Implies(Flip(a), Implies(a, b))
    steps = [
        Step([], rule_base_implies_false, {"a": b}),
        Step([0], rule_noncontradiction, {"a": a}),
        Step([0], rule_commutative_and),
        Step([], rule_portation),
    ]
    proof = StepProof(src, dst, steps)
    assert proof.verify()

