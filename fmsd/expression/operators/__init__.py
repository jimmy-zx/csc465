from fmsd.expression import Expression
from fmsd.expression.operator import Operator
from fmsd.expression.types import BinaryExpression


class BinaryOperator(Operator, BinaryExpression):
    pass


class BinaryOperator2WithBinaryOperands(BinaryOperator):
        def __init__(self, lhs: Expression, rhs: Expression) -> None:
            BinaryOperator.__init__(self, lhs, rhs)
            assert isinstance(lhs, BinaryExpression)
            assert isinstance(rhs, BinaryExpression)

        @property
        def lhs(self) -> Expression:
            return self.children[0]

        @property
        def rhs(self) -> Expression:
            return self.children[1]
