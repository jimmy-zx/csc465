import fmsd.utils.patch.binary
from fmsd.ast.node import Variable
from fmsd.utils.patchops.infix import EQ
from fmsd_impl.constants.basic import TRUE, FALSE

assert fmsd.utils.patch.binary


def test_basic():
    a = Variable("a")
    pattern = TRUE & a
    assert pattern.match(TRUE & a, {}) == {"a": a}
    assert pattern.match(TRUE & FALSE, {}) == {"a": FALSE}
    assert pattern.match(FALSE & a, {}) is None
    assert pattern.match(TRUE & (TRUE | FALSE), {}) == {"a": TRUE | FALSE}
    assert pattern.eval({"a": TRUE}) == TRUE & TRUE
    assert pattern.eval({"a": FALSE}) == TRUE & FALSE
    assert pattern.eval({}) == TRUE & a


def test_recursion():
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")
    pattern = a & (b | c)
    assert pattern.match(TRUE & (FALSE | TRUE), {}) == {
        "a": TRUE,
        "b": FALSE,
        "c": TRUE,
    }


def test_case():
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")
    pattern = a @ EQ @ b
    assert pattern.match(b @ EQ @ c, {}) == {"a": b, "b": c}
