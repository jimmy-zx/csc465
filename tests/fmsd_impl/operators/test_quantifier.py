import pytest

from fmsd.ast import VarNode
from fmsd_impl.constants import NAT, ONE
from fmsd_impl.operators import Exists, Forall, Function, Quantifier


def test_init():
    x = VarNode("x")
    y = VarNode("y")
    z = VarNode("z")
    assert Exists.from_func(x, NAT, x + ONE) == Exists(Function(x, NAT, x + ONE))
    assert Exists.from_list([(x, NAT), (y, ONE), (z, x)], x + y + z + ONE) == Exists(
        Function(
            x, NAT, Exists(Function(y, ONE, Exists(Function(z, x, x + y + z + ONE))))
        )
    )
    assert Quantifier.from_chain(
        [(Exists, x, NAT), (Forall, y, ONE), (Exists, z, x)], x + y + z + ONE
    ) == Exists(
        Function(
            x, NAT, Forall(Function(y, ONE, Exists(Function(z, x, x + y + z + ONE))))
        )
    )

    with pytest.raises(AssertionError):
        Quantifier()
