from fmsd.ast import Node, VarNode
from fmsd.ast_ext import Constant


def test_replace_with_meta():
    tree = Node(VarNode("a"), Constant("1"))
    assert tree.replace([1], VarNode("b")) == Node(VarNode("a"), VarNode("b"))
