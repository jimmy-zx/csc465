from fmsd.expression.constants.binary import TRUE, FALSE
from fmsd.expression.operators.binary import Implies, And, Flip
from fmsd.expression.variables import BinaryVariable
from fmsd.proof import ChainProof
from fmsd.proof.derived_step import TransformProof
from fmsd.rule.rules.binary import rule_portation, rule_noncontradiction, \
    rule_base_implies_false, rule_commutative_and
from fmsd.transform.expr import ExpressionTransform

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


def test_multi_step_proof():
    """
    Exercise 6c
    """
    src = Implies(Flip(a), Implies(a, b))
    dst = TRUE
    step1 = Implies(And(Flip(a), a), b)
    step2 = Implies(And(a, Flip(a)), b)
    step3 = Implies(FALSE, b)
    proof = ChainProof(src, dst, [
        TransformProof(src, step1, ExpressionTransform(rule_portation), []),
        TransformProof(step1, step2, ExpressionTransform(rule_commutative_and), [0]),
        TransformProof(step2, step3, ExpressionTransform(rule_noncontradiction), [0]),
        TransformProof(step3, dst, ExpressionTransform(rule_base_implies_false), []),
    ])
    assert proof.verify()


def test_multi_step_proof_rev():
    """
    Exercise 6c
    """
    src = TRUE
    dst = Implies(Flip(a), Implies(a, b))
    step1 = Implies(FALSE, b)
    step2 = Implies(And(a, Flip(a)), b)
    step3 = Implies(And(Flip(a), a), b)
    proof = ChainProof(src, dst, [
        TransformProof(src, step1, ExpressionTransform(rule_base_implies_false), []),
        TransformProof(step1, step2, ExpressionTransform(rule_noncontradiction), [0]),
        TransformProof(step2, step3, ExpressionTransform(rule_commutative_and), [0]),
        TransformProof(step3, dst, ExpressionTransform(rule_portation), []),
    ])
    assert proof.verify()
