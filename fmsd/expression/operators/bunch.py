from fmsd.expression.operators import (
    Operator2,
    Operator1,
    AssociativeOperator,
    CommutativeOperator,
    OperatorWithSameOp1AndReturnType,
    OperatorWithSameTypeOperands,
    OperatorWithNumericOperands,
)
from fmsd.expression.types import Binary, Numeric


class Union(
    OperatorWithSameOp1AndReturnType,
    OperatorWithSameTypeOperands,
    Operator2,
    AssociativeOperator,
    CommutativeOperator,
):
    DELIM = ","


class Intersect(
    OperatorWithSameOp1AndReturnType,
    OperatorWithSameTypeOperands,
    Operator2,
    AssociativeOperator,
    CommutativeOperator,
):
    DELIM = "‘"


class In(OperatorWithSameTypeOperands, Operator2, Binary):
    DELIM = ":"


class Includes(OperatorWithSameTypeOperands, Operator2, Binary):
    DELIM = "::"


class BunchInterval(OperatorWithNumericOperands, Operator2, Numeric):
    DELIM = ",.."


class Count(Operator1, Numeric):
    DELIM = "¢"
