from fmsd.ast import Variable
from fmsd.proof import DerivedEquivChainProof
from fmsd_impl.constants import FALSE, TRUE
from fmsd_impl.operators import Ternary


def test_ternary():
    x = Variable("x")
    y = Variable("y")
    assert DerivedEquivChainProof(
        Ternary(TRUE, x, y),
        x,
        [
            Ternary(TRUE, x, y),
            x,
        ],
    ).verify()
    assert DerivedEquivChainProof(
        Ternary(FALSE, x, y),
        y,
        [
            Ternary(FALSE, x, y),
            y,
        ],
    ).verify()
