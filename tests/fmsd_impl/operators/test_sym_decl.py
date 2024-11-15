import pytest

from fmsd.ast import Node, VarNode
from fmsd_impl.operators import SymbolDeclaration


def test_decl():
    x = VarNode("x")
    y = VarNode("y")
    tree = SymbolDeclaration(x, Node(y))
    assert tree.sym_decls() == {x}
    assert tree.sym_refs() == {y}


def test_construction():
    x = VarNode("x")
    y = VarNode("y")

    # variable of the same name can be declared multiple times,
    # given that they do not overlap
    Node(
        SymbolDeclaration(y, x),
        SymbolDeclaration(y, y),
    )

    # cannot refer to a variable that is declared elsewhere
    with pytest.raises(AssertionError):
        Node(
            Node(SymbolDeclaration(y, y)),
            Node(SymbolDeclaration(x, y)),
        )

    # nested declaration is allowed
    SymbolDeclaration(x, SymbolDeclaration(y, Node(x, y)))

    # shadowing is not allowed
    with pytest.raises(AssertionError):
        SymbolDeclaration(x, Node(SymbolDeclaration(x, x)))

    # any undeclared variable is global
    Node(x)
