import pytest

import fmsd_impl.patch
from fmsd.ast import Variable
from fmsd.proof import DerivedStepProof, NoTransformationFoundException
from fmsd_impl.constants import ONE

assert fmsd_impl.patch


def test_count():
    with pytest.raises(NoTransformationFoundException):
        DerivedStepProof(
            ONE + ONE + ONE, ONE + ONE,
        ).verify()
    a = Variable("a")
    b = Variable("b")
    assert DerivedStepProof(
        (a + b) + a, (a + a) + b
    ).verify()