from fmsd.expression.operators.generic import Equals, NotEquals
from fmsd.expression.operators.numeric import Max, Min
from fmsd.expression import Expression
from fmsd.utils.patchop import InfixOperator

# pylint: disable=invalid-name


# noinspection PyPep8Naming
@InfixOperator[Expression, Expression, Expression]
def EQ(lhs, rhs):
    return Equals(lhs, rhs)


# noinspection PyPep8Naming
@InfixOperator[Expression, Expression, Expression]
def NEQ(lhs, rhs):
    return NotEquals(lhs, rhs)


@InfixOperator[Expression, Expression, Expression]
def MAX(lhs, rhs):
    return Max(lhs, rhs)


@InfixOperator[Expression, Expression, Expression]
def MIN(lhs, rhs):
    return Min(lhs, rhs)


__all__ = [
    "EQ",
    "NEQ",
    "MAX",
    "MIN",
]
