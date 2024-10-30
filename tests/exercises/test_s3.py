from fmsd.ast.node import Variable
from fmsd.ast_ext import Constant
from fmsd.proof.derived import DerivedChainProof
from fmsd.utils.config import config
from fmsd_impl.constants.basic import TRUE, NAT, ZERO, INFINITY, ONE, NULL
from fmsd_impl.operators import Intersect, Count
from fmsd_impl.operators.bunch import In, Union
from fmsd_impl.operators.context import Context
from fmsd_impl.operators.generic import Equals
from fmsd_impl.operators.set_ import Size, Contents, Set, SetIn


def test_42():
    SEVEN = Constant("7")
    proof = DerivedChainProof(
        TRUE,
        ~In(SEVEN, NULL),
        [
            TRUE,
            Equals(Count(NULL), ZERO),
            Equals(Count(Intersect(NULL, SEVEN)), ZERO),
            Equals(Count(Intersect(SEVEN, NULL)), ZERO),
            ~In(SEVEN, NULL),
        ],
    )
    assert proof.verify()


def test_49a():
    n = Variable("n")
    config.trace = True
    proof = DerivedChainProof(
        In(n, NAT),
        In(ZERO, n * NAT),
        [
            In(n, NAT),
            In(n, NAT) & In(n, NAT),
            (n < INFINITY) & (n >= ZERO),
            (n < INFINITY) & ((n >= ZERO) & TRUE),
            (n < INFINITY) & ((n >= ZERO) & (-INFINITY < ZERO)),
            (n < INFINITY) & ((ZERO <= n) & (-INFINITY < ZERO)),
            (n < INFINITY) & ((-INFINITY < ZERO) & (ZERO <= n)),
            (n < INFINITY) & (-INFINITY < n),
            (-INFINITY < n) & (n < INFINITY),
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
    m = Variable("m")
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


def test_49d():
    m = Variable("m")
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


def test_55a():
    S = Variable("S")
    proof = DerivedChainProof(
        TRUE,
        Equals(Size(S), Count(Contents(S))),
        [
            TRUE,
            Equals(Size(Set(Contents(S))), Count(Contents(S))),
            Equals(Size(S), Count(Contents(S))),
        ],
    )
    assert proof.verify()


def test_55b():
    A = Variable("A")
    S = Variable("S")
    proof = DerivedChainProof(
        SetIn(A, S),
        In(A, Contents(S)),
        [SetIn(A, S), SetIn(A, Set(Contents(S))), In(A, Contents(S))],
    )
    assert proof.verify()
