from fmsd.expression import Expression
from fmsd.expression.constants import TRUE, FALSE
from fmsd.expression.operators.binary import Equals, And, NotEquals, Flip, Ternary


def rule_reflexivity(exp: Expression, x: Expression | None = None) -> Expression:
    if isinstance(exp, Equals):
        assert exp.lhs == exp.rhs
        return TRUE
    if exp == TRUE:
        assert x is not None
        return Equals(x, x)
    assert False


def rule_symmetry(exp: Expression) -> Expression:
    assert isinstance(exp, Equals)
    return Equals(exp.rhs, exp.lhs)


def rule_transitivity(exp: Expression) -> Expression:
    assert isinstance(exp, And)
    assert isinstance(exp.lhs, Equals)
    assert isinstance(exp.rhs, Equals)
    assert exp.lhs.rhs == exp.rhs.lhs
    return Equals(exp.lhs.lhs, exp.rhs.rhs)


def rule_unequality(exp: Expression) -> Expression:
    if isinstance(exp, NotEquals):
        return Flip(Equals(exp.lhs, exp.rhs))
    if isinstance(exp, Flip):
        assert isinstance(exp.op, Equals)
        return NotEquals(exp.op.lhs, exp.op.rhs)
    assert False


def rule_case_base(exp: Expression) -> Expression:
    assert isinstance(exp, Ternary)
    if exp.operands[0] == TRUE:
        return exp.operands[1]
    if exp.operands[0] == FALSE:
        return exp.operands[2]
    assert False


def rule_case_idempotent(exp: Expression) -> Expression:
    assert isinstance(exp, Ternary)
    assert exp.operands[1] == exp.operands[2]
    return exp.operands[1]


def rule_case_reversal(exp: Expression) -> Expression:
    assert isinstance(exp, Ternary)
    return Ternary(Flip(exp.operands[0]), exp.operands[2], exp.operands[1])
