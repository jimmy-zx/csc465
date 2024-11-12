from fmsd.ast import VarNode
from fmsd.proof import DerivedEquivChainProof
from fmsd_impl.constants import FALSE, TRUE
from fmsd_impl.operators import Ternary


def test_ternary():
    x = VarNode("x")
    y = VarNode("y")
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
