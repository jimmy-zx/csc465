import pytest

import fmsd_impl.patch
from fmsd.ast import VarNode
from fmsd.proof import DerivedStepProof, NoTransformationFoundException
from fmsd_impl.constants import ONE

assert fmsd_impl.patch


def test_count():
    with pytest.raises(NoTransformationFoundException):
        DerivedStepProof(
            ONE + ONE + ONE,
            ONE + ONE,
        ).verify()
    a = VarNode("a")
    b = VarNode("b")
    assert DerivedStepProof((a + b) + a, (a + a) + b).verify()


def test_idempotent():
    a = VarNode("a")
    b = VarNode("b")
    assert DerivedStepProof(a, a & a & a).verify()
    assert DerivedStepProof(
        a & b,
        a & (a & b) & (b & b),
    ).verify()
