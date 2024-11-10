from fmsd.ast_ext import Constant
from fmsd.proof import DerivedEquivChainProof, DynamicProofFactory
from fmsd_impl.constants import NAT, ONE, TRUE, ZERO
from fmsd_impl.operators import (
    Context,
    Equals,
    In,
    Join,
    Length,
    List,
    ListAt,
    ListCompose,
    ListLength,
    ListReplace,
    Replace,
    Set,
    StringRange,
    Subscript,
    Union,
)


def test_list_bunch():
    two = Constant("2")
    ten = Constant("10")
    s1 = Join.bin_list(ZERO, ONE, two).copy()
    s2 = Join.bin_list(NAT, ONE, StringRange(ZERO, ten)).copy()
    assert DerivedEquivChainProof(
        Context(In(List(s1), List(s2)), In(s1, s2)),
        Context(TRUE, In(s1, s2)),
        [
            Context(In(List(s1), List(s2)), In(s1, s2)),
            Context(In(List(s1), List(s2)), Equals(Union(s1, s2), s2)),
            Context(In(List(s1), List(Union(s1, s2))), Equals(Union(s1, s2), s2)),
            Context(In(List(s1), List(Union(s1, s2))), In(s1, s2)),
            Context(In(List(s1), Union(List(s1), List(s2))), In(s1, s2)),
            Context(
                Equals(
                    Union(List(s1), Union(List(s1), List(s2))),
                    Union(List(s1), List(s2)),
                ),
                In(s1, s2),
            ),
            Context(
                Equals(Union(List(s1), List(s2)), Union(List(s1), List(s2))), In(s1, s2)
            ),
            Context(TRUE, In(s1, s2)),
        ],
    ).verify()


def test_length():
    a = Constant("3")
    b = Constant("5")
    c = Constant("7")
    d = Constant("4")
    s = Join.bin_list(a, b, c, d).copy()
    assert DerivedEquivChainProof(
        Context(ListLength(List(s)), Equals(Length(s), d)),
        Context(d, Equals(Length(s), d)),
        [
            Context(ListLength(List(s)), Equals(Length(s), d)),
            Context(Length(s), Equals(Length(s), d)),
            Context(d, Equals(Length(s), d)),
        ],
    ).verify()


def test_compose_element():
    a = Constant("3")
    b = Constant("5")
    c = Constant("7")
    d = Constant("4")
    s = Join.bin_list(a, b, c, d).copy()
    two = Constant("2")
    assert DerivedEquivChainProof(
        Context(ListCompose(List(s), two), Equals(Subscript(s, two), c)),
        Context(c, Equals(Subscript(s, two), c)),
        [
            Context(ListCompose(List(s), two), Equals(Subscript(s, two), c)),
            Context(Subscript(s, two), Equals(Subscript(s, two), c)),
            Context(c, Equals(Subscript(s, two), c)),
        ],
    ).verify()


def test_compose_list():
    a = Constant("3")
    b = Constant("5")
    c = Constant("7")
    d = Constant("4")
    two = Constant("2")
    s = Join.bin_list(a, b, c, d).copy()
    i = Join.bin_list(two, ONE, two).copy()
    r = Join.bin_list(c, b, c).copy()
    assert DerivedEquivChainProof(
        Context(ListCompose(List(s), List(i)), Equals(Subscript(s, i), r)),
        Context(List(r), Equals(Subscript(s, i), r)),
        [
            Context(ListCompose(List(s), List(i)), Equals(Subscript(s, i), r)),
            Context(List(Subscript(s, i)), Equals(Subscript(s, i), r)),
            Context(List(r), Equals(Subscript(s, i), r)),
        ],
    ).verify()


def test_compose_mult():
    a = Constant("10")
    b = Constant("11")
    c = Constant("12")
    two = Constant("2")
    s = Join.bin_list(a, b, c).copy()
    assert DerivedEquivChainProof(
        Subscript(
            s,
            Union(ZERO, Set(Union(ONE, Join(List(Join(two, ONE)), ZERO)))),
        ),
        Union(a, Set(Union(b, Join(List(Join(c, b)), a)))),
        [
            Subscript(
                s,
                Union(ZERO, Set(Union(ONE, Join(List(Join(two, ONE)), ZERO)))),
            ),
            Union(
                Subscript(s, ZERO),
                Subscript(s, Set(Union(ONE, Join(List(Join(two, ONE)), ZERO)))),
            ),
            Union(
                Subscript(s, ZERO),
                Set(Subscript(s, Union(ONE, Join(List(Join(two, ONE)), ZERO)))),
            ),
            Union(
                Subscript(s, ZERO),
                Set(
                    Union(
                        Subscript(s, ONE),
                        Subscript(s, Join(List(Join(two, ONE)), ZERO)),
                    )
                ),
            ),
            Union(
                Subscript(s, ZERO),
                Set(
                    Union(
                        Subscript(s, ONE),
                        Join(Subscript(s, List(Join(two, ONE))), Subscript(s, ZERO)),
                    )
                ),
            ),
            Union(
                Subscript(s, ZERO),
                Set(
                    Union(
                        Subscript(s, ONE),
                        Join(List(Subscript(s, Join(two, ONE))), Subscript(s, ZERO)),
                    )
                ),
            ),
            Union(
                Subscript(s, ZERO),
                Set(
                    Union(
                        Subscript(s, ONE),
                        Join(
                            List(Join(Subscript(s, two), Subscript(s, ONE))),
                            Subscript(s, ZERO),
                        ),
                    )
                ),
            ),
            Union(a, Set(Union(b, Join(List(Join(c, b)), a)))),
        ],
    ).verify()


def test_replace():
    a = Constant("10")
    b = Constant("11")
    c = Constant("12")
    d = Constant("13")
    e = Constant("14")
    f = Constant("15")
    two = Constant("2")
    target = Constant("22")
    assert DerivedEquivChainProof(
        ListReplace(two, target, List(StringRange(a, f))),
        List(Join.bin_list(a, b, target, d, e)),
        [
            ListReplace(two, target, List(StringRange(a, f))),
            ListReplace(two, target, List(Join.bin_list(a, b, c, d, e))),
            List(Replace(Join.bin_list(a, b, c, d, e), two, target)),
            List(Join.bin_list(a, b, target, d, e)),
        ],
    ).verify()
    three = Constant("3")
    target1 = Constant("33")
    assert DerivedEquivChainProof(
        ListReplace(two, target, ListReplace(three, target1, List(StringRange(a, f)))),
        List(Join.bin_list(a, b, target, target1, e)),
        [
            ListReplace(
                two, target, ListReplace(three, target1, List(StringRange(a, f)))
            ),
            ListReplace(
                two,
                target,
                ListReplace(three, target1, List(Join.bin_list(a, b, c, d, e))),
            ),
            ListReplace(
                two, target, List(Replace(Join.bin_list(a, b, c, d, e), three, target1))
            ),
            ListReplace(two, target, List(Join.bin_list(a, b, c, target1, e))),
            List(Replace(Join.bin_list(a, b, c, target1, e), two, target)),
            List(Join.bin_list(a, b, target, target1, e)),
        ],
    ).verify()


def test_at():
    a = Constant("2")
    b = Constant("3")
    c = Constant("4")
    d = Constant("5")
    e = Constant("6")
    f = Constant("7")
    l1 = List(Join(a, b)).copy()
    l2 = List(Join(e, f)).copy()
    l3 = List(Join(d, l2)).copy()
    idx = Join(a, Join(ONE, ZERO))
    z = DynamicProofFactory()
    z.s(ListAt(List(Join.bin_list(l1, c, l3)), idx))
    z.s(ListAt(ListAt(List(Join.bin_list(l1, c, l3)), a), Join(ONE, ZERO)))
    z.s(
        ListAt(
            Context(ListAt(List(Join.bin_list(l1, c, l3)), a), TRUE), Join(ONE, ZERO)
        )
    )
    z.s(
        ListAt(
            Context(ListAt(List(Join.bin_list(l1, c, l3)), a), Equals(Length(a), ONE)),
            Join(ONE, ZERO),
        )
    )
    z.s(
        ListAt(
            Context(
                ListCompose(List(Join.bin_list(l1, c, l3)), a), Equals(Length(a), ONE)
            ),
            Join(ONE, ZERO),
        )
    )
    z.s(
        ListAt(
            Context(ListCompose(List(Join.bin_list(l1, c, l3)), a), TRUE),
            Join(ONE, ZERO),
        )
    )
    z.s(ListAt(ListCompose(List(Join.bin_list(l1, c, l3)), a), Join(ONE, ZERO)))
    z.s(ListAt(Subscript(Join.bin_list(l1, c, l3), a), Join(ONE, ZERO)))
    z.s(ListAt(l3, Join(ONE, ZERO)))
    z.s(ListAt(ListAt(l3, ONE), ZERO))
    z.s(ListAt(Context(ListAt(l3, ONE), TRUE), ZERO))
    z.s(ListAt(Context(ListAt(l3, ONE), Equals(Length(ONE), ONE)), ZERO))
    z.s(ListAt(Context(ListCompose(l3, ONE), Equals(Length(ONE), ONE)), ZERO))
    z.s(ListAt(Context(ListCompose(l3, ONE), TRUE), ZERO))
    z.s(ListAt(ListCompose(l3, ONE), ZERO))
    z.s(ListAt(Subscript(Join(d, l2), ONE), ZERO))
    z.s(ListAt(l2, ZERO))
    z.s(Context(ListAt(l2, ZERO), TRUE))
    z.s(
        Context(
            ListAt(l2, ZERO),
            Equals(Length(ZERO), ONE),
        )
    )
    z.s(
        Context(
            ListCompose(l2, ZERO),
            Equals(Length(ZERO), ONE),
        )
    )
    z.s(
        Context(
            ListCompose(l2, ZERO),
            TRUE,
        )
    )
    z.s(ListCompose(l2, ZERO))
    z.s(Subscript(Join(e, f), ZERO))
    z.s(e)
    assert z.generate(DerivedEquivChainProof).verify()


def test_replace_multi():
    a = Constant("2")
    b = Constant("3")
    c = Constant("4")
    d = Constant("5")
    e = Constant("6")
    l1 = List(Join.bin_list(ZERO, ONE, a)).copy()
    l2 = List(Join.bin_list(b, c, d)).copy()
    l3 = List(Join(l1, l2)).copy()
    idx = Join(ZERO, ONE)
    z = DynamicProofFactory()
    z.s(ListReplace(idx, e, l3))
    z.s(ListReplace(ZERO, ListReplace(ONE, e, ListAt(l3, ZERO)), l3))
    z.s(ListReplace(ZERO, ListReplace(ONE, e, l1), l3))
    z.s(ListReplace(ZERO, List(Replace(Join.bin_list(ZERO, ONE, a), ONE, e)), l3))
    z.s(ListReplace(ZERO, List(Join.bin_list(ZERO, e, a)), l3))
    z.s(
        ListReplace(
            ZERO,
            List(Join.bin_list(ZERO, e, a)),
            List(Join(l1, l2)),
        )
    )
    z.s(
        List(
            Replace(
                Join(l1, l2),
                ZERO,
                List(Join.bin_list(ZERO, e, a)),
            )
        )
    )
    z.s(List(Join(List(Join.bin_list(ZERO, e, a)), l2)))
    assert z.generate(DerivedEquivChainProof).verify()
