from fmsd.expression.operators.binary import Implies, And, Flip
from fmsd.expression.operators.generic import Equals
from fmsd.expression.variables import BinaryVariable
from fmsd.proof import ChainProof
from fmsd.proof.derived_step import TransformProof
from fmsd.transform.transforms.axioms.binary import (
    axiom_conflation_and,
    axiom_specialization,
)
from fmsd.transform.transforms.axioms.binary_generic import axiom_symmetry
from fmsd.transform.expr import ExpressionTransform

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


def test_child():
    """
    Exercise 6e
    """
    src = Equals(Equals(a, Implies(a, b)), And(a, b))
    dst = Equals(Equals(Implies(a, b), a), And(a, b))
    proof = TransformProof(src, dst, ExpressionTransform(axiom_symmetry), [0])
    assert proof.verify()


def test_root():
    """
    Exercise 6f
    """
    src = And(Implies(a, c), Implies(b, Flip(c)))
    dst = Implies(And(a, b), And(c, Flip(c)))
    proof = TransformProof(src, dst, ExpressionTransform(axiom_conflation_and), [])
    assert proof.verify()


def test_single_step_proof():
    """
    Exercise 6g
    """
    src = And(a, Flip(b))
    dst = a
    proof = ChainProof(
        src,
        dst,
        [
            TransformProof(src, dst, ExpressionTransform(axiom_specialization), []),
        ],
    )
    assert proof.verify()
