import fmsd.expression.operators.binary as binop
import fmsd.expression.operators.numeric as numop
from fmsd.expression import Expression
from fmsd.expression.types import BinaryExpression, NumericExpression
from fmsd.utils.patchop import InfixOperator


# noinspection PyPep8Naming
@InfixOperator[Expression, Expression, BinaryExpression]
def EQ(lhs, rhs):
    if isinstance(lhs, BinaryExpression) and isinstance(rhs, BinaryExpression):
        return binop.Equals(lhs, rhs)
    if isinstance(lhs, NumericExpression) and isinstance(rhs, NumericExpression):
        return numop.Equals(lhs, rhs)
    raise NotImplementedError()


# noinspection PyPep8Naming
@InfixOperator[Expression, Expression, BinaryExpression]
def NEQ(lhs, rhs):
    if isinstance(lhs, BinaryExpression) and isinstance(rhs, BinaryExpression):
        return binop.NotEquals(lhs, rhs)
    if isinstance(lhs, NumericExpression) and isinstance(rhs, NumericExpression):
        return numop.NotEquals(lhs, rhs)
    raise NotImplementedError()


@InfixOperator[Expression, Expression, Expression]
def MAX(lhs, rhs):
    if isinstance(lhs, NumericExpression) and isinstance(rhs, NumericExpression):
        return numop.Max(lhs, rhs)
    raise NotImplementedError()


@InfixOperator[Expression, Expression, Expression]
def MIN(lhs, rhs):
    if isinstance(lhs, NumericExpression) and isinstance(rhs, NumericExpression):
        return numop.Min(lhs, rhs)
    raise NotImplementedError()


__all__ = [
    "EQ",
    "NEQ",
]
