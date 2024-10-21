from fmsd.expression import Expression
from fmsd.expression.constants.binary import TRUE, FALSE
from fmsd.expression.operators.binary import Flip, And, Or, Implies, ImpliedBy
from fmsd.expression.operators.generic import Equals, NotEquals, Ternary
from fmsd.expression.types import Type
from fmsd.transform.func import FunctionTransform


def func_rule_table(exp: Expression) -> Expression:  # pylint: disable=too-many-branches,too-many-return-statements
    assert exp.type() == Type.BINARY
    assert exp.is_constant()
    if isinstance(exp, Flip):
        if exp.op == TRUE:
            return FALSE
        return TRUE
    if isinstance(exp, And):
        if exp.lhs == TRUE and exp.rhs == TRUE:
            return TRUE
        return FALSE
    if isinstance(exp, Or):
        if exp.lhs == FALSE and exp.rhs == FALSE:
            return FALSE
        return TRUE
    if isinstance(exp, Implies):
        if exp.lhs == TRUE and exp.rhs == FALSE:
            return FALSE
        return TRUE
    if isinstance(exp, ImpliedBy):
        if exp.rhs == TRUE and exp.lhs == FALSE:
            return FALSE
        return TRUE
    if isinstance(exp, Equals):
        if exp.lhs == exp.rhs:
            return TRUE
        return FALSE
    if isinstance(exp, NotEquals):
        if exp.lhs != exp.rhs:
            return TRUE
        return FALSE
    if isinstance(exp, Ternary):
        if exp.children[0] == TRUE:
            return exp.children[1]
        return exp.children[2]
    assert False


def rule_table_wrapper(src: Expression, dst: Expression) -> bool:
    try:
        return func_rule_table(src) == dst
    except AssertionError:
        return False


t_rule_table = FunctionTransform(rule_table_wrapper)
