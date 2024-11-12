from fmsd.ast import VarNode
from fmsd_impl.operators import And


def test_and():
    a = VarNode("a")
    b = VarNode("b")
    c = VarNode("c")
    d = VarNode("d")
    e = VarNode("e")
    assert And.bin_list(a, b, c, d, e) == a & b & c & d & e
