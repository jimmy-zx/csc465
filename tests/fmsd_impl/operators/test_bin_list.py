from fmsd.ast import Variable
from fmsd_impl.operators import And


def test_and():
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")
    d = Variable("d")
    e = Variable("e")
    assert And.bin_list(a, b, c, d, e) == a & b & c & d & e
