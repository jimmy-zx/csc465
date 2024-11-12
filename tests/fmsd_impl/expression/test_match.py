import fmsd_impl.patch.binary
from fmsd.ast.node import VarNode
from fmsd_impl.constants.basic import FALSE, TRUE
from fmsd_impl.patch.infix import EQ

assert fmsd_impl.patch.binary


def test_basic():
    a = VarNode("a")
    pattern = TRUE & a
    assert pattern.match(TRUE & a, {}) == {a: a}
    assert pattern.match(TRUE & FALSE, {}) == {a: FALSE}
    assert pattern.match(FALSE & a, {}) is None
    assert pattern.match(TRUE & (TRUE | FALSE), {}) == {a: TRUE | FALSE}
    assert pattern.eval({a: TRUE}) == TRUE & TRUE
    assert pattern.eval({a: FALSE}) == TRUE & FALSE
    assert pattern.eval({}) == TRUE & a


def test_recursion():
    a = VarNode("a")
    b = VarNode("b")
    c = VarNode("c")
    pattern = a & (b | c)
    assert pattern.match(TRUE & (FALSE | TRUE), {}) == {
        a: TRUE,
        b: FALSE,
        c: TRUE,
    }


def test_case():
    a = VarNode("a")
    b = VarNode("b")
    c = VarNode("c")
    pattern = a @ EQ @ b
    assert pattern.match(b @ EQ @ c, {}) == {a: b, b: c}
