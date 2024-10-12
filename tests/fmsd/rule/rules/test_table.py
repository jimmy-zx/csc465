import pytest

from fmsd.expression.constants.binary import TRUE as T, FALSE as F
from fmsd.expression.operators.binary import Flip, And, Or, Implies, ImpliedBy, Equals, NotEquals, Ternary
from fmsd.expression.types import BinaryExpression
from fmsd.rule.rules.table import rule_table


@pytest.mark.parametrize(
    ("op", "operands", "res"),
    [
        (Flip, [T], F),
        (Flip, [F], T),
        (And, [T, T], T),
        (And, [T, F], F),
        (And, [F, T], F),
        (And, [F, F], F),
        (Or, [T, T], T),
        (Or, [T, F], T),
        (Or, [F, T], T),
        (Or, [F, F], F),
        (Implies, [T, T], T),
        (Implies, [T, F], F),
        (Implies, [F, T], T),
        (Implies, [F, F], T),
        (ImpliedBy, [T, T], T),
        (ImpliedBy, [T, F], T),
        (ImpliedBy, [F, T], F),
        (ImpliedBy, [F, F], T),
        (Equals, [T, T], T),
        (Equals, [T, F], F),
        (Equals, [F, T], F),
        (Equals, [F, F], T),
        (NotEquals, [T, T], F),
        (NotEquals, [T, F], T),
        (NotEquals, [F, T], T),
        (NotEquals, [F, F], F),
        (Ternary, [T, T, T], T),
        (Ternary, [T, T, F], T),
        (Ternary, [T, F, T], F),
        (Ternary, [T, F, F], F),
        (Ternary, [F, T, T], T),
        (Ternary, [F, T, F], F),
        (Ternary, [F, F, T], T),
        (Ternary, [F, F, F], F),
    ]
)
def test_table(op: type, operands: list[BinaryExpression], res: BinaryExpression):
    assert rule_table(op(*operands)) == res
