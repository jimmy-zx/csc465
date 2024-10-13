from fmsd.expression import Expression, VarTable
from fmsd.expression.constants.binary import TRUE, FALSE
from fmsd.expression.operators.binary import Flip, And, Or, Implies, ImpliedBy
from fmsd.expression.operators.generic import Equals, NotEquals, Ternary
from fmsd.expression.types import Type
from fmsd.rule import FunctionRule


def func_rule_table(exp: Expression, table: VarTable | None = None) -> Expression:
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


rule_table = FunctionRule(func_rule_table)
