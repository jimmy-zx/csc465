import pytest

from fmsd.ast import VarNode


def test_meta():
    a = VarNode("a")
    b = VarNode("b")
    c = VarNode(name="a")
    assert a != b
    assert a == c
    assert hash(a) != hash(b)
    assert hash(a) == hash(c)
    assert a == a.copy()
    with pytest.raises(AssertionError):
        VarNode()
    with pytest.raises(AssertionError):
        VarNode("a", "b")
    with pytest.raises(AssertionError):
        VarNode(name="a", other="b")
    with pytest.raises(AssertionError):
        VarNode(other="a")
