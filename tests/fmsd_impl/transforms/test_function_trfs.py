import pytest

from fmsd.ast import VarNode
from fmsd.ast_ext import Constant, Variable
from fmsd.impl.transforms import ExpressionTransform
from fmsd.proof import DerivedEquivChainProof, DynamicProofFactory
from fmsd_impl.constants import NAT, ONE, RAT, TRUE
from fmsd_impl.operators import (
    Context,
    Equals,
    Forall,
    Function,
    FunctionCompose,
    FunctionDomain,
    FunctionTo,
    In,
)
from fmsd_impl.transforms.axioms.function import axiom_extension
from fmsd_impl.transforms.function import t_rename


def test_application():
    n = Variable("n")
    three = Constant("3")
    z = DynamicProofFactory()
    z.s(FunctionCompose(Function(n, NAT, n + ONE), three))
    z.s(Context(FunctionCompose(Function(n, NAT, n + ONE), three), TRUE))
    z.s(Context(FunctionCompose(Function(n, NAT, n + ONE), three), In(three, NAT)))
    z.s(Context(three + ONE, In(three, NAT)))
    z.s(Context(three + ONE, TRUE))
    z.s(three + ONE)
    z.s(Constant("4"))
    assert z.generate(DerivedEquivChainProof).verify()


def test_complex_application():
    x = Variable("x")
    D = VarNode("D")
    with pytest.raises(AssertionError):
        Function(x, D, x + FunctionCompose(Function(x, D, x), x))


def test_rename():
    n = Variable("n")
    a = VarNode("a")
    assert t_rename.verify(
        Function(n, NAT, n + ONE),
        Function(a, NAT, FunctionCompose(Function(n, NAT, n + ONE), a)),
    )
    assert not t_rename.verify(
        Function(n, NAT, n + a),
        Function(a, NAT, FunctionCompose(Function(n, NAT, n + a), a)),
    )


def test_rename_as_theorem():
    v = VarNode("v")
    D = VarNode("D")
    w = VarNode("w")
    f = VarNode("f")
    z = DynamicProofFactory()
    z.s(Function(v, D, FunctionCompose(f, v)))
    z.s(
        Function(
            w,
            FunctionDomain(Function(v, D, FunctionCompose(f, v))),
            FunctionCompose(Function(v, D, FunctionCompose(f, v)), w),
        )
    )
    z.s(
        Function(
            w,
            FunctionDomain(Function(v, D, FunctionCompose(f, v))),
            FunctionCompose(Function(v, D, FunctionCompose(f, v)), w),
        )
    )
    z.s(Function(w, D, FunctionCompose(Function(v, D, FunctionCompose(f, v)), w)))
    z.s(
        Function(
            w,
            D,
            Context(
                FunctionCompose(Function(v, D, FunctionCompose(f, v)), w), In(w, D)
            ),
        )
    )
    z.s(Function(w, D, Context(FunctionCompose(f, w), In(w, D))))
    z.s(Function(w, D, FunctionCompose(f, w)))
    assert z.generate(DerivedEquivChainProof).verify()


def test_extension():
    v = VarNode("v")
    D = VarNode("D")
    b = VarNode("b")
    w = VarNode("w")
    assert ExpressionTransform(axiom_extension).verify(
        Function(v, D, b),
        Function(
            w, FunctionDomain(Function(v, D, b)), FunctionCompose(Function(v, D, b), w)
        ),
    )


def test_high_order_func():
    x = Variable("x")
    y = Variable("y")
    c3 = Constant("3")
    c5 = Constant("5")
    c2 = Constant("2")
    pf = DynamicProofFactory()
    pf.s(
        FunctionCompose(
            FunctionCompose(Function(x, RAT, Function(y, RAT, ((x + y) / c2))), c3), c5
        )
    )
    pf.s(
        FunctionCompose(
            Context(
                FunctionCompose(Function(x, RAT, Function(y, RAT, ((x + y) / c2))), c3),
                TRUE,
            ),
            c5,
        )
    )
    pf.s(
        FunctionCompose(
            Context(
                FunctionCompose(Function(x, RAT, Function(y, RAT, ((x + y) / c2))), c3),
                In(c3, RAT),
            ),
            c5,
        )
    )
    pf.s(FunctionCompose(Context(Function(y, RAT, ((c3 + y) / c2)), In(c3, RAT)), c5))
    pf.s(
        Context(
            FunctionCompose(
                Context(Function(y, RAT, ((c3 + y) / c2)), In(c3, RAT)), c5
            ),
            TRUE,
        )
    )
    pf.s(
        Context(
            FunctionCompose(
                Context(Function(y, RAT, ((c3 + y) / c2)), In(c3, RAT)), c5
            ),
            In(c5, RAT),
        )
    )
    pf.s(
        Context(
            FunctionCompose(
                Context(Function(y, RAT, ((c3 + y) / c2)), In(c3, RAT)), c5
            ),
            In(c5, RAT),
        )
    )
    pf.s(
        Context(
            FunctionCompose(Context(Function(y, RAT, ((c3 + y) / c2)), TRUE), c5),
            In(c5, RAT),
        )
    )
    pf.s(Context(FunctionCompose(Function(y, RAT, ((c3 + y) / c2)), c5), In(c5, RAT)))
    pf.s(Context((c3 + c5) / c2, In(c5, RAT)))
    pf.s(Context((c3 + c5) / c2, TRUE))
    pf.s((c3 + c5) / c2)
    pf.s(Constant("8") / c2)
    pf.s(Constant("4"))
    assert pf.generate(DerivedEquivChainProof).verify()


def test_one_point():
    n = Variable("n")
    c3 = Constant("3")
    c10 = Constant("10")
    pf = DynamicProofFactory()
    pf.s(Forall(Function(n, NAT, Equals(n, c3) >> (n < c10))))
    pf.s(Context(Forall(Function(n, NAT, Equals(n, c3) >> (n < c10))), TRUE))
    pf.s(Context(Forall(Function(n, NAT, Equals(n, c3) >> (n < c10))), In(c3, NAT)))
    pf.s(Context(FunctionCompose(Function(n, NAT, n < c10), c3), In(c3, NAT)))
    pf.s(Context(c3 < c10, In(c3, NAT)))
    pf.s(Context(c3 < c10, TRUE))
    pf.s(c3 < c10)
    pf.s(TRUE)
    assert pf.generate(DerivedEquivChainProof).verify()


def test_inclusion():
    n = Variable("n")
    x = Variable("x")
    y = Variable("y")
    pf = DynamicProofFactory()
    pf.s(In(Function(n, NAT, n + ONE), FunctionTo(NAT, NAT)))
    pf.s(In(Function(n, NAT, n + ONE), Function(x, NAT, NAT)))
    pf.s(
        In(
            FunctionDomain(Function(x, NAT, NAT)),
            FunctionDomain(Function(n, NAT, n + ONE)),
        )
        & Forall(
            Function(
                y,
                FunctionDomain(Function(x, NAT, NAT)),
                In(
                    FunctionCompose(Function(n, NAT, n + ONE), y),
                    FunctionCompose(Function(x, NAT, NAT), y),
                ),
            )
        )
    )
    pf.s(
        In(NAT, NAT)
        & Forall(
            Function(
                y,
                NAT,
                In(
                    FunctionCompose(Function(n, NAT, n + ONE), y),
                    FunctionCompose(Function(x, NAT, NAT), y),
                ),
            )
        )
    )
    pf.s(
        In(NAT, NAT)
        & Forall(
            Function(
                y,
                NAT,
                Context(
                    In(
                        FunctionCompose(Function(n, NAT, n + ONE), y),
                        FunctionCompose(Function(x, NAT, NAT), y),
                    ),
                    In(y, NAT),
                ),
            )
        )
    )
    pf.s(
        In(NAT, NAT)
        & Forall(
            Function(
                y,
                NAT,
                Context(
                    In(
                        Context(FunctionCompose(Function(n, NAT, n + ONE), y), TRUE),
                        Context(FunctionCompose(Function(x, NAT, NAT), y), TRUE),
                    ),
                    In(y, NAT),
                ),
            )
        )
    )
    pf.s(
        In(NAT, NAT)
        & Forall(
            Function(
                y,
                NAT,
                Context(
                    In(
                        Context(
                            FunctionCompose(Function(n, NAT, n + ONE), y), In(y, NAT)
                        ),
                        Context(FunctionCompose(Function(x, NAT, NAT), y), In(y, NAT)),
                    ),
                    In(y, NAT),
                ),
            )
        )
    )
    pf.s(
        In(NAT, NAT)
        & Forall(
            Function(
                y,
                NAT,
                Context(
                    In(Context(y + ONE, In(y, NAT)), Context(NAT, In(y, NAT))),
                    In(y, NAT),
                ),
            )
        )
    )
    pf.s(
        In(NAT, NAT)
        & Forall(
            Function(
                y,
                NAT,
                Context(In(Context(y + ONE, TRUE), Context(NAT, TRUE)), In(y, NAT)),
            )
        )
    )
    pf.s(
        In(NAT, NAT)
        & Forall(
            Function(
                y,
                NAT,
                Context(In(Context(y + ONE, TRUE), Context(NAT, TRUE)), In(y, NAT)),
            )
        )
    )
    pf.s(TRUE & Forall(Function(y, NAT, Context(In(y + ONE, NAT), In(y, NAT)))))
    pf.s(Forall(Function(y, NAT, Context(In(y + ONE, NAT), In(y, NAT)))))
    pf.s(Forall(Function(y, NAT, Context(In(y + ONE, NAT), In(y, NAT) & TRUE))))
    pf.s(Forall(Function(y, NAT, Context(In(y + ONE, NAT), In(y, NAT) & In(ONE, NAT)))))
    pf.s(Forall(Function(y, NAT, Context(In(y + ONE, NAT), In(y, NAT) & In(ONE, NAT)))))
    pf.s(
        Forall(
            Function(
                y,
                NAT,
                Context(Context(In(y + ONE, NAT), TRUE), In(y, NAT) & In(ONE, NAT)),
            )
        )
    )
    pf.s(
        Forall(
            Function(
                y,
                NAT,
                Context(
                    Context(
                        In(y + ONE, NAT),
                        (In(y, NAT) & In(ONE, NAT)) >> In(y + ONE, NAT),
                    ),
                    In(y, NAT) & In(ONE, NAT),
                ),
            )
        )
    )
    pf.s(
        Forall(
            Function(
                y,
                NAT,
                Context(
                    Context(In(y + ONE, NAT), TRUE >> In(y + ONE, NAT)),
                    In(y, NAT) & In(ONE, NAT),
                ),
            )
        )
    )
    pf.s(
        Forall(
            Function(
                y,
                NAT,
                Context(
                    Context(In(y + ONE, NAT), In(y + ONE, NAT)),
                    In(y, NAT) & In(ONE, NAT),
                ),
            )
        )
    )
    pf.s(
        Forall(
            Function(
                y,
                NAT,
                Context(Context(TRUE, In(y + ONE, NAT)), In(y, NAT) & In(ONE, NAT)),
            )
        )
    )
    pf.s(
        Forall(
            Function(
                y,
                NAT,
                Context(
                    Context(TRUE, TRUE >> In(y + ONE, NAT)), In(y, NAT) & In(ONE, NAT)
                ),
            )
        )
    )
    pf.s(
        Forall(
            Function(
                y,
                NAT,
                Context(
                    Context(TRUE, (In(y, NAT) & In(ONE, NAT)) >> In(y + ONE, NAT)),
                    In(y, NAT) & In(ONE, NAT),
                ),
            )
        )
    )
    pf.s(
        Forall(
            Function(y, NAT, Context(Context(TRUE, TRUE), In(y, NAT) & In(ONE, NAT)))
        )
    )
    pf.s(Forall(Function(y, NAT, Context(TRUE, In(y, NAT) & In(ONE, NAT)))))
    pf.s(Forall(Function(y, NAT, Context(TRUE, In(y, NAT) & TRUE))))
    pf.s(Forall(Function(y, NAT, Context(TRUE, In(y, NAT)))))
    pf.s(Forall(Function(y, NAT, TRUE)))
    pf.s(TRUE)
    assert pf.generate(DerivedEquivChainProof).verify()


def test_inclusion_to():
    n = Variable("n")
    pf = DynamicProofFactory()
    pf.s(In(Function(n, NAT, n + ONE), FunctionTo(NAT, NAT)))
    pf.s(
        In(NAT, FunctionDomain(Function(n, NAT, n + ONE)))
        & In(FunctionCompose(Function(n, NAT, n + ONE), NAT), NAT)
    )
    pf.s(In(NAT, NAT) & In(FunctionCompose(Function(n, NAT, n + ONE), NAT), NAT))
    pf.s(TRUE & In(FunctionCompose(Function(n, NAT, n + ONE), NAT), NAT))
    pf.s(In(FunctionCompose(Function(n, NAT, n + ONE), NAT), NAT))
    pf.s(In(Context(FunctionCompose(Function(n, NAT, n + ONE), NAT), TRUE), NAT))
    pf.s(
        In(Context(FunctionCompose(Function(n, NAT, n + ONE), NAT), In(NAT, NAT)), NAT)
    )
    pf.s(In(Context(NAT + ONE, In(NAT, NAT)), NAT))
    pf.s(In(Context(NAT + ONE, TRUE), NAT))
    pf.s(In(NAT + ONE, NAT))
    pf.s(TRUE)
    assert pf.generate(DerivedEquivChainProof).verify()
