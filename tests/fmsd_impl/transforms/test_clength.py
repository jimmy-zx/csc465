import pytest

from fmsd.ast import Node, VarNode
from fmsd.ast_ext import Constant
from fmsd.proof import DerivedEquivChainProof
from fmsd_impl.constants import INFINITY, ONE, TRUE, ZERO
from fmsd_impl.operators import (
    And,
    Context,
    Equals,
    ImpliedBy,
    Implies,
    Join,
    Length,
    Max,
    Min,
    Minus,
    Multiply,
    NotEquals,
    Or,
    Plus,
    Subscript,
)


def test_constant_length():
    assert DerivedEquivChainProof(
        TRUE, Equals(Length(ZERO), ONE), [TRUE, Equals(Length(ZERO), ONE)]
    ).verify()
    assert DerivedEquivChainProof(
        Length(ZERO),
        ONE,
        [
            Length(ZERO),
            Context(Length(ZERO), TRUE),
            Context(Length(ZERO), Equals(Length(ZERO), ONE)),
            Context(ONE, Equals(Length(ZERO), ONE)),
            Context(ONE, TRUE),
            ONE,
        ],
    ).verify()


def test_list_length():
    assert DerivedEquivChainProof(
        Length(Join(Join(ONE, ONE), Join(ONE, Join(ONE, ONE)))),
        Constant("5"),
        [
            Length(Join(Join(ONE, ONE), Join(ONE, Join(ONE, ONE)))),
            Length(Join(ONE, ONE)) + Length(Join(ONE, Join(ONE, ONE))),
            (Length(ONE) + Length(ONE)) + (Length(ONE) + Length(Join(ONE, ONE))),
            Length(ONE) + Length(ONE) + Length(ONE) + Length(Join(ONE, ONE)),
            Length(ONE) + Length(ONE) + Length(ONE) + (Length(ONE) + Length(ONE)),
            Length(ONE) + Length(ONE) + Length(ONE) + Length(ONE) + Length(ONE),
            Context(
                Length(ONE) + Length(ONE) + Length(ONE) + Length(ONE) + Length(ONE),
                TRUE,
            ),
            Context(
                Length(ONE) + Length(ONE) + Length(ONE) + Length(ONE) + Length(ONE),
                Equals(Length(ONE), ONE),
            ),
            Context(ONE + ONE + ONE + ONE + ONE, Equals(Length(ONE), ONE)),
            Context(ONE + ONE + ONE + ONE + ONE, TRUE),
            ONE + ONE + ONE + ONE + ONE,
            Constant("5"),
        ],
    ).verify()


def test_list_index():
    a = Constant("3")
    b = Constant("5")
    c = Constant("7")
    d = Constant("9")
    assert DerivedEquivChainProof(
        Length(Join(a, b)),
        Constant("2"),
        [
            Length(Join(a, b)),
            Length(a) + Length(b),
            ONE + ONE,
            Constant("2"),
        ],
    ).verify()

    two = Constant("2")
    left = Join(a, b).copy()
    s = Join(Join(left, c), d).copy()
    length = Equals(Length(left), two).copy()
    s_two = Subscript(s, two).copy()
    assert DerivedEquivChainProof(
        Context(s_two, length),
        Context(c, length),
        [
            Context(s_two, length),
            Context(Context(s_two, TRUE), length),
            Context(
                Context(
                    s_two,
                    ((Length(left) < INFINITY) & Equals(Length(c), ONE))
                    >> Equals(Subscript(s, Length(left)), c),
                ),
                length,
            ),
            Context(
                Context(
                    s_two,
                    ((two < INFINITY) & Equals(Length(c), ONE)) >> Equals(s_two, c),
                ),
                length,
            ),
            Context(Context(s_two, (TRUE & TRUE) >> Equals(s_two, c)), length),
            Context(Context(s_two, TRUE >> Equals(s_two, c)), length),
            Context(Context(s_two, Equals(s_two, c)), length),
            Context(Context(c, Equals(s_two, c)), length),
            Context(Context(c, TRUE >> Equals(s_two, c)), length),
            Context(Context(c, (TRUE & TRUE) >> Equals(s_two, c)), length),
            Context(
                Context(
                    c, ((two < INFINITY) & Equals(Length(c), ONE)) >> Equals(s_two, c)
                ),
                length,
            ),
            Context(
                Context(
                    c,
                    ((Length(left) < INFINITY) & Equals(Length(c), ONE))
                    >> Equals(Subscript(s, Length(left)), c),
                ),
                length,
            ),
            Context(Context(c, TRUE), length),
            Context(c, length),
        ],
    ).verify()


@pytest.mark.parametrize(
    "op",
    [
        And,
        Or,
        Implies,
        ImpliedBy,
        Equals,
        NotEquals,
        Plus,
        Minus,
        Multiply,
        Min,
        Max,
    ],
)
def test_op_length(op: type[Node]):
    x = VarNode("x")
    y = VarNode("y")
    assert DerivedEquivChainProof(
        (Equals(Length(x), ONE) & Equals(Length(y), ONE))
        >> Equals(Length(op(x, y)), ONE),
        TRUE,
        [
            (Equals(Length(x), ONE) & Equals(Length(y), ONE))
            >> Equals(Length(op(x, y)), ONE),
            TRUE,
        ],
    ).verify()
