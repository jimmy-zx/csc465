from fmsd.expression.constants.binary import TRUE
from fmsd.expression.constants.bunch import NAT
from fmsd.expression.constants.numeric import ZERO, INFINITY, NEG_INFINITY, ONE
from fmsd.expression.operators.bunch import In, Union
from fmsd.expression.operators.context import Context
from fmsd.expression.operators.generic import Equals
from fmsd.expression.variables import NumericSingularVariable
from fmsd.proof.derived_step import DerivedChainProof


def test_49a():
    n = NumericSingularVariable("n")
    proof = DerivedChainProof(
        In(n, NAT),
        In(ZERO, n * NAT),
        [
            In(n, NAT),
            In(n, NAT) & In(n, NAT),
            (n < INFINITY) & (n >= ZERO),
            (n < INFINITY) & ((n >= ZERO) & TRUE),
            (n < INFINITY) & ((n >= ZERO) & (NEG_INFINITY < ZERO)),
            (n < INFINITY) & ((ZERO <= n) & (NEG_INFINITY < ZERO)),
            (n < INFINITY) & ((NEG_INFINITY < ZERO) & (ZERO <= n)),
            (n < INFINITY) & (NEG_INFINITY < n),
            (NEG_INFINITY < n) & (n < INFINITY),
            Equals(n * ZERO, ZERO),
            Equals(ZERO, n * ZERO),
            In(ZERO, n * ZERO),
            In(ZERO, n * ZERO) & TRUE,
            In(ZERO, n * ZERO) & In(n * ZERO, Union(n * ZERO, n * NAT)),
            In(ZERO, Union(n * ZERO, n * NAT)),
            In(ZERO, n * Union(ZERO, NAT)),
            In(ZERO, n * Union(ZERO, NAT)) & TRUE,
            In(ZERO, n * Union(ZERO, NAT)) & In(ZERO, NAT),
            In(ZERO, n * Union(ZERO, NAT)) & Equals(Union(ZERO, NAT), NAT),
            Context(In(ZERO, n * Union(ZERO, NAT)), Equals(Union(ZERO, NAT), NAT))
            & Equals(Union(ZERO, NAT), NAT),
            Context(In(ZERO, n * NAT), Equals(Union(ZERO, NAT), NAT))
            & Equals(Union(ZERO, NAT), NAT),
            In(ZERO, n * NAT) & Equals(Union(ZERO, NAT), NAT),
            In(ZERO, n * NAT),
        ],
    )
    assert proof.verify()


def test_49b():
    m = NumericSingularVariable("m")
    proof = DerivedChainProof(
        # adding a local context here
        Context(In(m, ZERO * NAT), Equals(ZERO, ZERO * NAT)),
        Equals(m, ZERO),
        [
            Context(In(m, ZERO * NAT), Equals(ZERO, ZERO * NAT)),
            Context(In(m, ZERO), Equals(ZERO, ZERO * NAT)),
            In(m, ZERO),
            Equals(m, ZERO),
        ],
    )
    assert proof.verify()


def test_49c():
    # TODO: no proofs yet
    pass


def test_49d():
    m = NumericSingularVariable("m")
    proof = DerivedChainProof(
        Context(In(m, ONE * NAT), Equals(ONE * NAT, NAT)),
        In(m, NAT),
        [
            Context(In(m, ONE * NAT), Equals(ONE * NAT, NAT)),
            Context(In(m, NAT), Equals(ONE * NAT, NAT)),
            In(m, NAT),
        ],
    )
    assert proof.verify()
