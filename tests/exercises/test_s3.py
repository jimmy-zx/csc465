from fmsd.expression.operators.context import Context
from fmsd.expression.operators.generic import Equals
from fmsd.expression.variables import NumericSingularVariable
from fmsd.proof.derived_step import DerivedChainProof, DerivedStepProof
from fmsd.expression.operators.bunch import In, Union
from fmsd.expression.constants.bunch import NAT
from fmsd.expression.constants.binary import TRUE
from fmsd.expression.constants.numeric import ZERO, INFINITY, NEG_INFINITY


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
            Context(In(ZERO, n * Union(ZERO, NAT)), Equals(Union(ZERO, NAT), NAT)) & Equals(Union(ZERO, NAT), NAT),
            Context(In(ZERO, n * NAT), Equals(Union(ZERO, NAT), NAT)) & Equals(Union(ZERO, NAT), NAT),
            In(ZERO, n * NAT) & Equals(Union(ZERO, NAT), NAT),
            In(ZERO, n * NAT)
        ]
    )
    assert proof.verify()