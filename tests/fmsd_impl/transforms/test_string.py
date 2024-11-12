from fmsd.ast import Node, VarNode
from fmsd.ast_ext import Constant
from fmsd.proof import DerivedEquivChainProof
from fmsd_impl.constants import INFINITY, NAT, NIL, ONE, TRUE, ZERO
from fmsd_impl.operators import (
    And,
    BunchInterval,
    Context,
    Duplicate,
    Equals,
    Implies,
    In,
    Join,
    Length,
    Replace,
    Star,
    Subscript,
    Union,
)
from fmsd_impl.patch import EQ


def test_index_cnatural():
    a = Constant("3")
    b = Constant("5")
    c = Constant("7")
    d = Constant("9")
    f = Constant("2")
    assert DerivedEquivChainProof(
        Subscript(Join.bin_list(a, b, c, d), f),
        c,
        [
            Subscript(Join.bin_list(a, b, c, d), f),
            c,
        ],
    ).verify()


def test_index_string():
    a = Constant("3")
    b = Constant("5")
    c = Constant("7")
    d = Constant("9")
    e = Constant("1")
    f = Constant("2")
    s = Join.bin_list(a, b, c, d)
    s.copy_on_construction = True
    i = Join.bin_list(f, e, f)
    theorem1 = Equals(Subscript(s, e), b)
    theorem1.copy_on_construction = True
    theorem2 = Equals(Subscript(s, f), c)
    theorem2.copy_on_construction = True
    src = Context(Subscript(s, i), theorem1 & theorem2)
    dst = Context(Join.bin_list(c, b, c), theorem1 & theorem2)
    assert DerivedEquivChainProof(
        src,
        dst,
        [
            src,
            Context(
                Join(Subscript(s, Join(f, e)), Subscript(s, f)), theorem1 & theorem2
            ),
            Context(
                Join(Join(Subscript(s, f), Subscript(s, e)), Subscript(s, f)),
                theorem1 & theorem2,
            ),
            dst,
        ],
    ).verify()


def test_index_cstring():
    a = Constant("3")
    b = Constant("5")
    c = Constant("7")
    d = Constant("9")
    e = Constant("1")
    f = Constant("2")
    s = Join.bin_list(a, b, c, d)
    i = Join.bin_list(f, e, f)
    r = Join.bin_list(c, b, c)
    s.copy_on_construction = True
    i.copy_on_construction = True
    assert DerivedEquivChainProof(
        Subscript(s, i),
        r,
        [
            Subscript(s, i),
            r,
        ],
    ).verify()


def test_duplicate():
    s = Join(ZERO, ONE)
    s.copy_on_construction = True
    three = Constant("3")
    assert DerivedEquivChainProof(
        Duplicate(three, s),
        Join.bin_list(s, s, s),
        [
            Duplicate(three, s),
            Duplicate(ONE + ONE + ONE, s),
            Join(Duplicate(ONE + ONE, s), s),
            Join(Join(Duplicate(ONE, s), s), s),
            Join(Join(Duplicate(ZERO + ONE, s), s), s),
            Join(Join(Join(Duplicate(ZERO, s), s), s), s),
            Join(Join(Join(NIL, s), s), s),
            Join(Join(s, s), s),
            Join.bin_list(s, s, s),
        ],
    ).verify()


def test_replace():
    three = Constant("3")
    five = Constant("5")
    nine = Constant("9")
    eight = Constant("8")
    two = Constant("2")
    left = Join(three, five).copy()
    cond_eight = Equals(Length(eight), ONE).copy()
    cond_nine = Equals(Length(nine), ONE).copy()
    cond_two = (Length(left) < INFINITY).copy()
    assert DerivedEquivChainProof(
        Replace(Join(Join(left, eight), NIL), Length(left), nine),
        Join(Join(left, nine), NIL),
        [
            Replace(Join(Join(left, eight), NIL), Length(left), nine),
            Context(Replace(Join(Join(left, eight), NIL), Length(left), nine), TRUE),
            Context(
                Replace(Join(Join(left, eight), NIL), Length(left), nine),
                (cond_two & (cond_eight & cond_nine))
                >> Equals(
                    Replace(Join(Join(left, eight), NIL), Length(left), nine),
                    Join(Join(left, nine), NIL),
                ),
            ),
            Context(
                Replace(Join(Join(left, eight), NIL), Length(left), nine),
                ((two < INFINITY) & (TRUE & TRUE))
                >> Equals(
                    Replace(Join(Join(left, eight), NIL), Length(left), nine),
                    Join(Join(left, nine), NIL),
                ),
            ),
            Context(
                Replace(Join(Join(left, eight), NIL), Length(left), nine),
                (TRUE & (TRUE & TRUE))
                >> Equals(
                    Replace(Join(Join(left, eight), NIL), Length(left), nine),
                    Join(Join(left, nine), NIL),
                ),
            ),
            Context(
                Replace(Join(Join(left, eight), NIL), Length(left), nine),
                TRUE
                >> Equals(
                    Replace(Join(Join(left, eight), NIL), Length(left), nine),
                    Join(Join(left, nine), NIL),
                ),
            ),
            Context(
                Replace(Join(Join(left, eight), NIL), Length(left), nine),
                Equals(
                    Replace(Join(Join(left, eight), NIL), Length(left), nine),
                    Join(Join(left, nine), NIL),
                ),
            ),
            Context(
                Join(Join(left, nine), NIL),
                Equals(
                    Replace(Join(Join(left, eight), NIL), Length(left), nine),
                    Join(Join(left, nine), NIL),
                ),
            ),
            Context(
                Join(Join(left, nine), NIL),
                TRUE
                >> Equals(
                    Replace(Join(Join(left, eight), NIL), Length(left), nine),
                    Join(Join(left, nine), NIL),
                ),
            ),
            Context(
                Join(Join(left, nine), NIL),
                (TRUE & (TRUE & TRUE))
                >> Equals(
                    Replace(Join(Join(left, eight), NIL), Length(left), nine),
                    Join(Join(left, nine), NIL),
                ),
            ),
            Context(
                Join(Join(left, nine), NIL),
                ((two < INFINITY) & (cond_eight & cond_nine))
                >> Equals(
                    Replace(Join(Join(left, eight), NIL), Length(left), nine),
                    Join(Join(left, nine), NIL),
                ),
            ),
            Context(
                Join(Join(left, nine), NIL),
                (cond_two & (cond_eight & cond_nine))
                >> Equals(
                    Replace(Join(Join(left, eight), NIL), Length(left), nine),
                    Join(Join(left, nine), NIL),
                ),
            ),
            Context(Join(Join(left, nine), NIL), TRUE),
            Join(Join(left, nine), NIL),
        ],
    ).verify()


def test_ordering():
    three = Constant("3")
    six = Constant("6")
    four = Constant("4")
    seven = Constant("7")
    two = Constant("2")
    assert isinstance(seven < seven, Node)
    # noinspection PyTypeChecker
    assert DerivedEquivChainProof(
        Join.bin_list(three, six, four, seven) < Join.bin_list(three, seven, two),
        TRUE,
        [
            Join.bin_list(three, six, four, seven) < Join.bin_list(three, seven, two),
            Context(
                Join.bin_list(three, six, four, seven)
                < Join.bin_list(three, seven, two),
                TRUE,
            ),
            Context(
                Join.bin_list(three, six, four, seven)
                < Join.bin_list(three, seven, two),
                Implies(
                    And(
                        (Length(three) < INFINITY) & (six < seven),
                        Equals(Length(six), ONE) & Equals(Length(seven), ONE),
                    ),
                    Join(Join(three, six), Join(four, seven))
                    < Join(Join(three, seven), two),
                ),
            ),
            Context(
                Join.bin_list(three, six, four, seven)
                < Join.bin_list(three, seven, two),
                Implies(
                    And((ONE < INFINITY) & TRUE, TRUE & TRUE),
                    Join(Join(three, six), Join(four, seven))
                    < Join(Join(three, seven), two),
                ),
            ),
            Context(
                Join(Join(three, six), Join(four, seven))
                < Join(Join(three, seven), two),
                Implies(
                    And(TRUE & TRUE, TRUE & TRUE),
                    Join(Join(three, six), Join(four, seven))
                    < Join(Join(three, seven), two),
                ),
            ),
            Context(
                Join(Join(three, six), Join(four, seven))
                < Join(Join(three, seven), two),
                Implies(
                    TRUE,
                    Join(Join(three, six), Join(four, seven))
                    < Join(Join(three, seven), two),
                ),
            ),
            Context(
                Join(Join(three, six), Join(four, seven))
                < Join(Join(three, seven), two),
                Join(Join(three, six), Join(four, seven))
                < Join(Join(three, seven), two),
            ),
            Context(
                TRUE,
                Join(Join(three, six), Join(four, seven))
                < Join(Join(three, seven), two),
            ),
            Context(
                TRUE,
                TRUE
                >> (
                    Join(Join(three, six), Join(four, seven))
                    < Join(Join(three, seven), two)
                ),
            ),
            Context(
                TRUE,
                ((TRUE & TRUE) & (TRUE & TRUE))
                >> (
                    Join(Join(three, six), Join(four, seven))
                    < Join(Join(three, seven), two)
                ),
            ),
            Context(
                TRUE,
                (
                    ((ONE < INFINITY) & (six < seven))
                    & ((Length(six) @ EQ @ ONE) & (Length(seven) @ EQ @ ONE))
                )
                >> (
                    Join(Join(three, six), Join(four, seven))
                    < Join(Join(three, seven), two)
                ),
            ),
            Context(
                TRUE,
                (
                    ((Length(three) < INFINITY) & (six < seven))
                    & ((Length(six) @ EQ @ ONE) & (Length(seven) @ EQ @ ONE))
                )
                >> (
                    Join(Join(three, six), Join(four, seven))
                    < Join(Join(three, seven), two)
                ),
            ),
            Context(TRUE, TRUE),
            TRUE,
        ],
    ).verify()


def test_bunch_join():
    two = Constant("2")
    ten = Constant("10")
    assert DerivedEquivChainProof(
        In(
            Join.bin_list(ZERO, ONE, two),
            Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
        ),
        TRUE,
        [
            In(
                Join.bin_list(ZERO, ONE, two),
                Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
            ),
            Context(
                In(
                    Join.bin_list(ZERO, ONE, two),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
                TRUE,
            ),
            Context(
                In(
                    Join.bin_list(ZERO, ONE, two),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
                In(ZERO, NAT),
            ),
            Context(
                In(
                    Join.bin_list(ZERO, ONE, two),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
                Equals(Union(ZERO, NAT), NAT),
            ),
            Context(
                In(
                    Join.bin_list(ZERO, ONE, two),
                    Join.bin_list(Union(ZERO, NAT), ONE, BunchInterval(ZERO, ten)),
                ),
                Equals(Union(ZERO, NAT), NAT),
            ),
            Context(
                In(
                    Join.bin_list(ZERO, ONE, two),
                    Join.bin_list(Union(ZERO, NAT), ONE, BunchInterval(ZERO, ten)),
                ),
                In(ZERO, NAT),
            ),
            Context(
                In(
                    Join.bin_list(ZERO, ONE, two),
                    Join.bin_list(Union(ZERO, NAT), ONE, BunchInterval(ZERO, ten)),
                ),
                TRUE,
            ),
            In(
                Join.bin_list(ZERO, ONE, two),
                Join.bin_list(Union(ZERO, NAT), ONE, BunchInterval(ZERO, ten)),
            ),
            In(
                Join.bin_list(ZERO, ONE, two),
                Join(Union(ZERO, NAT), Join(ONE, BunchInterval(ZERO, ten))),
            ),
            In(
                Join.bin_list(ZERO, ONE, two),
                Union(
                    Join(ZERO, Join(ONE, BunchInterval(ZERO, ten))),
                    Join(NAT, Join(ONE, BunchInterval(ZERO, ten))),
                ),
            ),
            In(
                Join.bin_list(ZERO, ONE, two),
                Union(
                    Join.bin_list(ZERO, ONE, BunchInterval(ZERO, ten)),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
            ),
            In(
                Join.bin_list(ZERO, ONE, two),
                Union(
                    Context(Join.bin_list(ZERO, ONE, BunchInterval(ZERO, ten)), TRUE),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
            ),
            In(
                Join.bin_list(ZERO, ONE, two),
                Union(
                    Context(
                        Join.bin_list(ZERO, ONE, BunchInterval(ZERO, ten)),
                        In(two, BunchInterval(ZERO, ten)),
                    ),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
            ),
            In(
                Join.bin_list(ZERO, ONE, two),
                Union(
                    Context(
                        Join.bin_list(ZERO, ONE, BunchInterval(ZERO, ten)),
                        Equals(
                            Union(two, BunchInterval(ZERO, ten)),
                            BunchInterval(ZERO, ten),
                        ),
                    ),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
            ),
            In(
                Join.bin_list(ZERO, ONE, two),
                Union(
                    Context(
                        Join.bin_list(ZERO, ONE, Union(two, BunchInterval(ZERO, ten))),
                        Equals(
                            Union(two, BunchInterval(ZERO, ten)),
                            BunchInterval(ZERO, ten),
                        ),
                    ),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
            ),
            In(
                Join.bin_list(ZERO, ONE, two),
                Union(
                    Context(
                        Join.bin_list(ZERO, ONE, Union(two, BunchInterval(ZERO, ten))),
                        In(two, BunchInterval(ZERO, ten)),
                    ),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
            ),
            In(
                Join.bin_list(ZERO, ONE, two),
                Union(
                    Context(
                        Join.bin_list(ZERO, ONE, Union(two, BunchInterval(ZERO, ten))),
                        TRUE,
                    ),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
            ),
            In(
                Join.bin_list(ZERO, ONE, two),
                Union(
                    Join.bin_list(ZERO, ONE, Union(two, BunchInterval(ZERO, ten))),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
            ),
            In(
                Join.bin_list(ZERO, ONE, two),
                Union(
                    Union(
                        Join.bin_list(ZERO, ONE, two),
                        Join.bin_list(ZERO, ONE, BunchInterval(ZERO, ten)),
                    ),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
            ),
            Equals(
                Union(
                    Join.bin_list(ZERO, ONE, two),
                    Union(
                        Union(
                            Join.bin_list(ZERO, ONE, two),
                            Join.bin_list(ZERO, ONE, BunchInterval(ZERO, ten)),
                        ),
                        Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                    ),
                ),
                Union(
                    Union(
                        Join.bin_list(ZERO, ONE, two),
                        Join.bin_list(ZERO, ONE, BunchInterval(ZERO, ten)),
                    ),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
            ),
            Equals(
                Union(
                    Union(
                        Join.bin_list(ZERO, ONE, two),
                        Join.bin_list(ZERO, ONE, BunchInterval(ZERO, ten)),
                    ),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
                Union(
                    Union(
                        Join.bin_list(ZERO, ONE, two),
                        Join.bin_list(ZERO, ONE, BunchInterval(ZERO, ten)),
                    ),
                    Join.bin_list(NAT, ONE, BunchInterval(ZERO, ten)),
                ),
            ),
            TRUE,
        ],
    ).verify()


def test_star():
    a = VarNode("a")
    b = VarNode("b")
    s = Join(a, b).copy()
    two = Constant("2")
    assert DerivedEquivChainProof(
        In(Join(s, s), Star(s)),
        TRUE,
        [
            In(Join(s, s), Star(s)),
            In(Join(s, s), Duplicate(NAT, s)),
            Context(In(Join(s, s), Duplicate(NAT, s)), TRUE),
            Context(In(Join(s, s), Duplicate(NAT, s)), In(two, NAT)),
            Context(In(Join(s, s), Duplicate(NAT, s)), Equals(Union(two, NAT), NAT)),
            Context(
                In(Join(s, s), Duplicate(Union(two, NAT), s)),
                Equals(Union(two, NAT), NAT),
            ),
            Context(In(Join(s, s), Duplicate(Union(two, NAT), s)), In(two, NAT)),
            Context(In(Join(s, s), Duplicate(Union(two, NAT), s)), TRUE),
            In(Join(s, s), Duplicate(Union(two, NAT), s)),
            In(Join(s, s), Union(Duplicate(two, s), Duplicate(NAT, s))),
            In(Join(s, s), Union(Duplicate(ONE + ONE, s), Duplicate(NAT, s))),
            In(Join(s, s), Union(Join(Duplicate(ONE, s), s), Duplicate(NAT, s))),
            In(Join(s, s), Union(Join(Duplicate(ZERO + ONE, s), s), Duplicate(NAT, s))),
            In(
                Join(s, s),
                Union(Join(Join(Duplicate(ZERO, s), s), s), Duplicate(NAT, s)),
            ),
            In(Join(s, s), Union(Join(Join(NIL, s), s), Duplicate(NAT, s))),
            In(Join(s, s), Union(Join(s, s), Duplicate(NAT, s))),
            Equals(
                Union(Join(s, s), Union(Join(s, s), Duplicate(NAT, s))),
                Union(Join(s, s), Duplicate(NAT, s)),
            ),
            Equals(
                Union(Join(s, s), Duplicate(NAT, s)),
                Union(Join(s, s), Duplicate(NAT, s)),
            ),
            TRUE,
        ],
    ).verify()


def test_bunch_duplicate():
    two = Constant("2")
    assert DerivedEquivChainProof(
        Duplicate(two, Union(ZERO, ONE)),
        Union.bin_list(
            Join(ZERO, ZERO), Join(ZERO, ONE), Join(ONE, ZERO), Join(ONE, ONE)
        ),
        [
            Duplicate(two, Union(ZERO, ONE)),
            Duplicate(ONE + ONE, Union(ZERO, ONE)),
            Join(Duplicate(ONE, Union(ZERO, ONE)), Union(ZERO, ONE)),
            Join(Duplicate(ZERO + ONE, Union(ZERO, ONE)), Union(ZERO, ONE)),
            Join(
                Join(Duplicate(ZERO, Union(ZERO, ONE)), Union(ZERO, ONE)),
                Union(ZERO, ONE),
            ),
            Join(Join(NIL, Union(ZERO, ONE)), Union(ZERO, ONE)),
            Join(Union(ZERO, ONE), Union(ZERO, ONE)),
            Union(Join(ZERO, Union(ZERO, ONE)), Join(ONE, Union(ZERO, ONE))),
            Union(
                Union(Join(ZERO, ZERO), Join(ZERO, ONE)),
                Union(Join(ONE, ZERO), Join(ONE, ONE)),
            ),
            Union.bin_list(
                Join(ZERO, ZERO), Join(ZERO, ONE), Join(ONE, ZERO), Join(ONE, ONE)
            ),
        ],
    ).verify()
