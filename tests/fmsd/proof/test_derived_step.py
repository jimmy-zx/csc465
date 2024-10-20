import pytest

import fmsd.utils.patch.binary
from fmsd.expression.constants.binary import TRUE
from fmsd.expression.operators.binary import Or
from fmsd.expression.operators.generic import Equals
from fmsd.expression.variables import BinaryVariable
from fmsd.proof.derived_step import (
    DerivedStepProof,
    DerivedChainProof,
    DerivedEquivChainProof,
)
from fmsd.utils import config
from fmsd.utils.patchops.infix import EQ

assert fmsd.utils.patch.binary

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


def test_simple():
    proof = DerivedStepProof(a & b, b & a)
    assert proof.verify()


def test_invalid():
    proof = DerivedStepProof(a & b, b & c)
    with pytest.raises(Exception):
        assert proof.verify()


def test_mult():
    proof = DerivedStepProof((a | b) & (a | c), (b | a) & (c | a))
    assert proof.verify()


def test_deep():
    src = ((a & b) & b) & b
    dst = ((b & a) & b) & b
    proof = DerivedStepProof(src, dst)
    assert proof.verify()


def test_multiple():
    """
    Exercise 6m
    """
    src = (a >> ~a) >> ~a
    dst = TRUE
    proof = DerivedChainProof(src, dst, [src, (~a | ~a) >> ~a, ~a >> ~a, dst])
    assert proof.verify()


def test_multiple_equiv():
    """
    Exercise 6p
    """
    src = Or(Equals(a, b), Or(Equals(a, c), Equals(b, c)))
    dst = TRUE
    config.config.trace = True
    proof = DerivedEquivChainProof(
        src,
        dst,
        [
            src,
            Or(Equals(a, b), Or(Equals(a, c), Equals(b, Equals(TRUE, c)))),
            Or(Equals(a, b), Or(Equals(a, c), Equals(b, Equals(c, TRUE)))),
            Or(Equals(a, b), Or(Equals(a, c), Equals(b, Equals(TRUE, c)))),
            Or(Equals(a, b), Or(Equals(a, c), Equals(b, Equals(Equals(a, a), c)))),
            Or(Equals(a, b), Or(Equals(a, c), Equals(b, Equals(a, Equals(a, c))))),
            Or(Equals(a, b), Or(Equals(a, c), Equals(Equals(b, a), Equals(a, c)))),
            Or(Or(Equals(a, b), Equals(a, c)), Equals(Equals(b, a), Equals(a, c))),
            Equals(
                Or(Or(Equals(a, b), Equals(a, c)), Equals(b, a)),
                Or(Or(Equals(a, b), Equals(a, c)), Equals(a, c)),
            ),
            Equals(
                Or(Or(Equals(a, b), Equals(a, c)), Equals(a, b)),
                Or(Or(Equals(a, b), Equals(a, c)), Equals(a, c)),
            ),
            Equals(
                Or(Or(Equals(a, c), Equals(a, b)), Equals(a, b)),
                Or(Or(Equals(a, b), Equals(a, c)), Equals(a, c)),
            ),
            Equals(
                Or(Equals(a, c), Or(Equals(a, b), Equals(a, b))),
                Or(Or(Equals(a, b), Equals(a, c)), Equals(a, c)),
            ),
            Equals(
                Or(Equals(a, c), Or(Equals(a, b), Equals(a, b))),
                Or(Equals(a, b), Or(Equals(a, c), Equals(a, c))),
            ),
            Equals(
                Or(Equals(a, c), Equals(a, b)),
                Or(Equals(a, b), Or(Equals(a, c), Equals(a, c))),
            ),
            Equals(Or(Equals(a, c), Equals(a, b)), Or(Equals(a, b), Equals(a, c))),
            Equals(Or(Equals(a, b), Equals(a, c)), Or(Equals(a, b), Equals(a, c))),
            dst,
        ],
    )
    config.config.trace = False
    assert proof.verify()
    print(proof.formalize())


def test_parallel():
    """
    Exercise 6s
    """
    src = ((a >> (a & b)) @ EQ @ (a >> b)) & ((a >> b) @ EQ @ ((a | b) >> b))
    dst = TRUE
    proof = DerivedEquivChainProof(
        src,
        dst,
        [
            ((a >> (a & b)) @ EQ @ (a >> b)) & ((a >> b) @ EQ @ ((a | b) >> b)),
            (((a >> a) & (a >> b)) @ EQ @ (a >> b))
            & ((a >> b) @ EQ @ ((a >> b) & (b >> b))),
            ((TRUE & (a >> b)) @ EQ @ (a >> b)) & ((a >> b) @ EQ @ ((a >> b) & TRUE)),
            ((a >> b) @ EQ @ (a >> b)) & ((a >> b) @ EQ @ (a >> b)),
            TRUE & TRUE,
            TRUE,
        ],
    )
    assert proof.verify()


def test_chain():
    src = Equals(Equals(a, b >> a), a | b)
    dst = TRUE
    proof = DerivedEquivChainProof(
        src,
        dst,
        [
            src,
            Equals(a | b, Equals(a, b >> a)),
            Equals(Equals(a | b, a), b >> a),
            Equals(Equals(b | a, a), b >> a),
            Equals(b >> a, b >> a),
            dst,
        ],
    )
    assert proof.verify()
