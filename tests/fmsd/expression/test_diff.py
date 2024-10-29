import pytest

import fmsd_impl.patch.binary
from fmsd.ast.node import Node, Variable

assert fmsd_impl.patch.binary

a = Variable("a")
b = Variable("b")
c = Variable("c")


@pytest.mark.parametrize(
    ("lhs", "rhs", "idx"),
    [
        ((a | b) & c, a & c, [0]),
        ((a & b) & c, (a & (a | b)) & c, [0, 1]),
        (a & b, b & a, []),
    ],
)
def test_symmetric_diff(lhs: Node, rhs: Node, idx: list[int] | None):
    assert lhs.diff(rhs) == idx
    assert rhs.diff(lhs) == idx


@pytest.mark.parametrize(
    ("lhs", "rhs"),
    [
        ((a | b) & c, (a | b) & c),
    ],
)
def test_no_diff(lhs: Node, rhs: Node):
    assert lhs.diff(rhs) is None
    assert rhs.diff(lhs) is None


def test_start():
    lhs = (a & b) & c
    rhs = ((a | b) & b) & (a | c)
    assert lhs.diff(rhs) == []
    assert rhs.diff(lhs) == []


def test_mult_diff():
    lhs = (a | b) & (a | c)
    rhs = (b | a) & (b | c)
    assert lhs.diff(rhs) == []
