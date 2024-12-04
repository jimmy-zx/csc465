import pytest

from fmsd.ast import VarNode
from fmsd.impl.operators import SymbolDeclaration, Top
from fmsd_impl.constants import NAT, ONE
from fmsd_impl.operators import Exists, Function


def test_top():
    with pytest.raises(AssertionError):
        Top(VarNode("a"))
    with pytest.raises(AssertionError):
        Top(SymbolDeclaration(VarNode("a"), VarNode("b")))
    Top(SymbolDeclaration(VarNode("a"), VarNode("a")))
    Top(Exists(Function(VarNode("a"), NAT, VarNode("a") + ONE)))
