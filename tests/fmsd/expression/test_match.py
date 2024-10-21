import fmsd.utils.patch.binary
from fmsd.expression.constants.binary import TRUE, FALSE
from fmsd.expression.variables import BinaryVariable, NumericVariable, NumericSingularVariable
from fmsd.utils.patchops.infix import EQ

assert fmsd.utils.patch.binary


def test_basic():
    a = BinaryVariable("a")
    pattern = TRUE & a
    assert (TRUE & FALSE).match(pattern, {}) == {"a": FALSE}
    assert (FALSE & a).match(pattern, {}) is None
    assert (TRUE & a).match(pattern, {}) == {"a": a}
    assert (TRUE & (TRUE | FALSE)).match(pattern, {}) == {"a": TRUE | FALSE}
    assert pattern.eval_var({"a": TRUE}) == TRUE & TRUE
    assert pattern.eval_var({"a": FALSE}) == TRUE & FALSE
    assert pattern.eval_var({}) == TRUE & a


def test_recursion():
    a = BinaryVariable("a")
    b = BinaryVariable("b")
    c = BinaryVariable("c")
    pattern = a & (b | c)
    assert (TRUE & (FALSE | TRUE)).match(pattern, {}) == {"a": TRUE, "b": FALSE, "c": TRUE}


def test_case():
    a = BinaryVariable("a")
    b = BinaryVariable("b")
    c = BinaryVariable("c")
    pattern = a @ EQ @ b
    assert (b @ EQ @ c).match(pattern, {}) == {"a": b, "b": c}


def test_typing():
    a = BinaryVariable("a")
    b = BinaryVariable("b")
    x = NumericVariable("x")
    y = NumericVariable("y")
    assert a.match(x, {}) is None
    assert a.match(a, {}) == {"a": a}
    assert (a @ EQ @ b).match(x @ EQ @ y, {}) is None


def test_singular():
    num = NumericVariable("num")
    sin = NumericSingularVariable("sin")
    assert num.match(num, {}) == {"num": num}
    assert sin.match(num, {}) == {"num": sin}
    assert num.match(sin, {}) is None
    assert sin.match(sin, {}) == {"sin": sin}
