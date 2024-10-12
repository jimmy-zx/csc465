import fmsd.expression.operators.binary as binop
from fmsd.expression.types import BinaryExpression
from fmsd.utils.patchop import InfixOperator


BinaryInfixOperator = InfixOperator[BinaryExpression, BinaryExpression, BinaryExpression]


# noinspection PyPep8Naming
@BinaryInfixOperator
def Equals(lhs, rhs):
    if isinstance(lhs, BinaryExpression) and isinstance(rhs, BinaryExpression):
        return binop.Equals(lhs, rhs)
    raise NotImplementedError()


# noinspection PyPep8Naming
@BinaryInfixOperator
def NotEquals(lhs, rhs):
    if isinstance(lhs, BinaryExpression) and isinstance(rhs, BinaryExpression):
        return binop.NotEquals(lhs, rhs)


__all__ = [
    "Equals",
    "NotEquals",
]
