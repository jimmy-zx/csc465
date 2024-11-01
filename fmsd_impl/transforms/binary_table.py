from fmsd.ast.node import Node
from fmsd.transform.transform import FunctionTransform
from fmsd_impl.constants import TRUE, FALSE
from fmsd_impl.operators import (
    Flip,
    And,
    Or,
    Implies,
    ImpliedBy,
    Equals,
    NotEquals,
    Ternary,
)


def func_rule_table(
    exp: Node,
) -> Node:
    # pylint: disable=too-many-branches,too-many-return-statements  # noqa: E501
    assert all(node in {TRUE, FALSE} for node in exp.nodes)
    if isinstance(exp, Flip):
        if exp.nodes[0] == TRUE:
            return FALSE
        return TRUE
    if isinstance(exp, And):
        if exp.nodes[0] == TRUE and exp.nodes[1] == TRUE:
            return TRUE
        return FALSE
    if isinstance(exp, Or):
        if exp.nodes[0] == FALSE and exp.nodes[1] == FALSE:
            return FALSE
        return TRUE
    if isinstance(exp, Implies):
        if exp.nodes[0] == TRUE and exp.nodes[1] == FALSE:
            return FALSE
        return TRUE
    if isinstance(exp, ImpliedBy):
        if exp.nodes[1] == TRUE and exp.nodes[0] == FALSE:
            return FALSE
        return TRUE
    if isinstance(exp, Equals):
        if exp.nodes[0] == exp.nodes[1]:
            return TRUE
        return FALSE
    if isinstance(exp, NotEquals):
        if exp.nodes[0] != exp.nodes[1]:
            return TRUE
        return FALSE
    if isinstance(exp, Ternary):
        if exp.nodes[0] == TRUE:
            return exp.nodes[1]
        return exp.nodes[2]
    assert False


def rule_table_wrapper(src: Node, dst: Node) -> bool:
    try:
        return func_rule_table(src) == dst
    except AssertionError:
        return False


t_rule_table = FunctionTransform(rule_table_wrapper)
