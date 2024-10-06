from fmsd.expression.constants import TRUE, FALSE
from fmsd.expression.variables import BinaryVariable
from fmsd.expression.operators.binary import And, Or

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")

def test_basic():
    pattern = And(TRUE, a)
    assert And(TRUE, FALSE).match(pattern, {}) == {"a": FALSE}
    assert And(FALSE, BinaryVariable("a")).match(pattern, {}) is None
    assert And(TRUE, a).match(pattern, {}) == {"a": a}
    assert And(TRUE, Or(TRUE, FALSE)).match(pattern, {}) == {"a": Or(TRUE, FALSE)}
    assert pattern.eval_var({"a": TRUE}) == And(TRUE, TRUE)
    assert pattern.eval_var({"a": FALSE}) == And(TRUE, FALSE)
    assert pattern.eval_var({}) == And(TRUE, BinaryVariable("a"))


def test_recursion():
    pattern = And(a, Or(b, c))
    assert And(TRUE, Or(FALSE, TRUE)).match(pattern, {}) == {"a": TRUE, "b": FALSE, "c": TRUE}
