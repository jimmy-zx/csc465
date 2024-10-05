from fmsd.expression.operators import (
    Operator1,
    Operator2,
    OperatorWithBinaryOperands,
    AssociativeOperator,
    CommutativeOperator,
)
from fmsd.expression.types import Binary


class Flip(OperatorWithBinaryOperands, Operator1, Binary):
    DELIM = "¬"


class And(
    OperatorWithBinaryOperands,
    Operator2,
    Binary,
    AssociativeOperator,
    CommutativeOperator,
):
    DELIM = "∧"


class Or(
    OperatorWithBinaryOperands,
    Operator2,
    Binary,
    AssociativeOperator,
    CommutativeOperator,
):
    DELIM = "∨"


class Implies(OperatorWithBinaryOperands, Operator2, Binary):
    DELIM = "⇒"


class ImpliedBy(OperatorWithBinaryOperands, Operator2, Binary):
    DELIM = "⇐"
