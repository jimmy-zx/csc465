from fmsd.expression import Expression
from fmsd.expression.constants import TRUE, FALSE
from fmsd.expression.operators.binary import Equals, And, NotEquals, Flip, Or, Implies, ImpliedBy


def rule_excluded_middle(exp: Expression, a: Expression | None = None) -> Expression:
    if isinstance(exp, Or):
        assert isinstance(exp.rhs, Flip)
        assert exp.lhs == exp.rhs.op
        return TRUE
    assert exp == TRUE
    assert a is not None
    return Or(a, Flip(a))


def rule_noncontradiction(exp: Expression, a: Expression | None = None) -> Expression:
    if isinstance(exp, And):
        assert isinstance(exp.rhs, Flip)
        assert exp.lhs == exp.rhs.op
        return FALSE
    assert exp == FALSE
    assert a is not None
    return And(a, Flip(a))


def rule_base(exp: Expression) -> Expression:
    if isinstance(exp, And):
        assert exp.rhs == FALSE
        return FALSE
    if isinstance(exp, Or):
        assert exp.rhs == TRUE
        return TRUE
    if isinstance(exp, Implies):
        if exp.rhs == TRUE:
            return TRUE
        if exp.lhs == FALSE:
            return TRUE
    assert False
    # TODO: construction


def rule_mirror(exp: Expression) -> Expression:
    if isinstance(exp, Implies):
        return ImpliedBy(exp.rhs, exp.lhs)
    if isinstance(exp, ImpliedBy):
        return Implies(exp.rhs, exp.lhs)
    assert False


def rule_double_negation(exp: Expression) -> Expression:
    if isinstance(exp, Flip):
        assert isinstance(exp.op, Flip)
        return exp.op.op
    return Flip(Flip(exp))


def rule_duality(exp: Expression) -> Expression:
    if isinstance(exp, Flip):
        if isinstance(exp.op, And):
            return Or(Flip(exp.op.lhs), Flip(exp.op.rhs))
        if isinstance(exp.op, Or):
            return And(Flip(exp.op.lhs), Flip(exp.op.rhs))
    assert False


def rule_exclusion(exp: Expression) -> Expression:
    if isinstance(exp, Implies):
        return Implies(Flip(exp.rhs), Flip(exp.lhs))
    if isinstance(exp, Equals):
        assert isinstance(exp.rhs, Flip)
        return NotEquals(exp.lhs, exp.rhs.op)
    if isinstance(exp, NotEquals):
        return Equals(exp.lhs, Flip(exp.rhs))
    assert False


def rule_material_implication(exp: Expression) -> Expression:
    if isinstance(exp, Implies):
        return Or(Flip(exp.lhs), exp.rhs)
    if isinstance(exp, Or):
        return Implies(Flip(exp.lhs), exp.rhs)
    assert False


def rule_inclusion_and(exp: Expression) -> Expression:
    if isinstance(exp, Implies):
        return Equals(And(exp.lhs, exp.rhs), exp.lhs)
    if isinstance(exp, Equals):
        assert isinstance(exp.lhs, And)
        assert exp.lhs.lhs == exp.rhs
        return Implies(exp.lhs.lhs, exp.lhs.rhs)


def rule_inclusion_or(exp: Expression) -> Expression:
    if isinstance(exp, Implies):
        return Equals(Or(exp.lhs, exp.rhs), exp.rhs)
    if isinstance(exp, Equals):
        assert isinstance(exp.lhs, Or)
        assert exp.lhs.rhs == exp.rhs
        return Implies(exp.lhs.lhs, exp.lhs.rhs)
