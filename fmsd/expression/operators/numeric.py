from fmsd.expression.operators import (
    Operator1,
    Operator2,
    OperatorWithNumericOperands,
    AssociativeOperator,
    CommutativeOperator,
)
from fmsd.expression.types import Numeric, Binary


class Negate(OperatorWithNumericOperands, Operator1, Numeric):
    DELIM = "-"


class Plus(
    OperatorWithNumericOperands,
    Operator2,
    Numeric,
    AssociativeOperator,
    CommutativeOperator,
):
    DELIM = "+"


class Minus(OperatorWithNumericOperands, Operator2, Numeric):
    DELIM = "-"


class Multiply(
    OperatorWithNumericOperands,
    Operator2,
    Numeric,
    AssociativeOperator,
    CommutativeOperator,
):
    DELIM = "×"


class DividedBy(OperatorWithNumericOperands, Operator2, Numeric):
    DELIM = "/"


class Power(OperatorWithNumericOperands, Operator2, Numeric):
    DELIM = "^"


class Max(
    OperatorWithNumericOperands,
    Operator2,
    Numeric,
    AssociativeOperator,
    CommutativeOperator,
):
    DELIM = "↑"


class Min(
    OperatorWithNumericOperands,
    Operator2,
    Numeric,
    AssociativeOperator,
    CommutativeOperator,
):
    DELIM = "↓"


class LessThan(OperatorWithNumericOperands, Operator2, Binary):
    DELIM = "<"


class LessThanOrEqualsTo(OperatorWithNumericOperands, Operator2, Binary):
    DELIM = "≤"


class GreaterThan(OperatorWithNumericOperands, Operator2, Binary):
    DELIM = ">"


class GreaterThanOrEqualsTo(OperatorWithNumericOperands, Operator2, Binary):
    DELIM = "≥"
