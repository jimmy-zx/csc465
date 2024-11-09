import pytest

from fmsd.ast import Node, Variable
from fmsd.ast_ext import Constant
from fmsd.proof import DerivedEquivChainProof
from fmsd_impl.constants import ONE, TRUE, ZERO
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
    )


def test_list_length():
    assert DerivedEquivChainProof(
        Length(Join(Join(ONE, ONE), Join(ONE, Join(ONE, ONE)))),
        Constant("5"),
        [
            Length(Join(Join(ONE, ONE), Join(ONE, Join(ONE, ONE)))),
            Length(Join(ONE, ONE)) + Length(Join(ONE, Join(ONE, ONE))),
            Length(ONE) + Length(ONE) + Length(ONE) + Length(Join(ONE, ONE)),
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
    )


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
    )
    theorem_length = Equals(Length(Join(a, b)), Constant("2"))
    join_form = Join(Join(Join(a, b), c), d)
    theorem_length.copy_on_construction = True
    join_form.copy_on_construction = True
    assert DerivedEquivChainProof(
        Context(Subscript(Join(a, Join(b, Join(c, d))), Constant("2")), theorem_length),
        Context(c, theorem_length),
        [
            Context(
                Subscript(Join(a, Join(b, Join(c, d))), Constant("2")), theorem_length
            ),
            Context(join_form, theorem_length),
            Context(Context(join_form, TRUE), theorem_length),
            Context(
                Context(join_form, Implies(theorem_length, Equals(join_form, c))),
                theorem_length,
            ),
            Context(Context(join_form, Equals(join_form, c)), theorem_length),
            Context(Context(c, Equals(join_form, c)), theorem_length),
            Context(
                Context(c, Implies(theorem_length, Equals(join_form, c))),
                theorem_length,
            ),
            Context(Context(c, TRUE), theorem_length),
            Context(c, theorem_length),
        ],
    )


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
    x = Variable("x")
    y = Variable("y")
    assert DerivedEquivChainProof(
        (Equals(Length(x), ONE) & Equals(Length(y), ONE))
        >> Equals(Length(op(x, y)), ONE),
        TRUE,
        [
            (Equals(Length(x), ONE) & Equals(Length(y), ONE))
            >> Equals(Length(op(x, y)), ONE),
            TRUE,
        ],
    )
