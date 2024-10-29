from fmsd.ast.node import Variable
from fmsd.proof.chain import ChainProof
from fmsd.proof.transform import TransformProof
from fmsd_impl.transforms.expr import ExpressionTransform
from fmsd_impl.transforms.axioms.binary import (
    axiom_portation,
    axiom_noncontradiction,
    axiom_base_implies_false,
    axiom_commutative_and,
)
from fmsd_impl.constants.basic import TRUE, FALSE
from fmsd_impl.operators.binary import Implies, And, Flip

a = Variable("a")
b = Variable("b")
c = Variable("c")


def test_multi_step_proof():
    """
    Exercise 6c
    """
    src = Implies(Flip(a), Implies(a, b))
    dst = TRUE
    step1 = Implies(And(Flip(a), a), b)
    step2 = Implies(And(a, Flip(a)), b)
    step3 = Implies(FALSE, b)
    proof = ChainProof(
        src,
        dst,
        [
            TransformProof(src, step1, ExpressionTransform(axiom_portation), []),
            TransformProof(
                step1, step2, ExpressionTransform(axiom_commutative_and), [0]
            ),
            TransformProof(
                step2, step3, ExpressionTransform(axiom_noncontradiction), [0]
            ),
            TransformProof(
                step3, dst, ExpressionTransform(axiom_base_implies_false), []
            ),
        ],
    )
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
    proof = ChainProof(
        src,
        dst,
        [
            TransformProof(
                src, step1, ExpressionTransform(axiom_base_implies_false), []
            ),
            TransformProof(
                step1, step2, ExpressionTransform(axiom_noncontradiction), [0]
            ),
            TransformProof(
                step2, step3, ExpressionTransform(axiom_commutative_and), [0]
            ),
            TransformProof(step3, dst, ExpressionTransform(axiom_portation), []),
        ],
    )
    assert proof.verify()
