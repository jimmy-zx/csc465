# noinspection PyUnresolvedReferences
import fmsd.utils.patch.binary
from fmsd.expression.constants.binary import TRUE, FALSE
from fmsd.expression.variables import BinaryVariable
from fmsd.utils.patchops.infix import EQ

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


def test_basic():
    pattern = TRUE & a
    assert (TRUE & FALSE).match(pattern, {}) == {"a": FALSE}
    assert (FALSE & a).match(pattern, {}) is None
    assert (TRUE & a).match(pattern, {}) == {"a": a}
    assert (TRUE & (TRUE | FALSE)).match(pattern, {}) == {"a": TRUE | FALSE}
    assert pattern.eval_var({"a": TRUE}) == TRUE & TRUE
    assert pattern.eval_var({"a": FALSE}) == TRUE & FALSE
    assert pattern.eval_var({}) == TRUE & a


def test_recursion():
    pattern = a & (b | c)
    assert (TRUE & (FALSE | TRUE)).match(pattern, {}) == {"a": TRUE, "b": FALSE, "c": TRUE}


def test_case():
    pattern = a @ EQ @ b
    assert (b @ EQ @ c).match(pattern, {}) == {"a": b, "b": c}
