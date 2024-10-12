from fmsd.expression import Expression
from fmsd.expression.operators import NumericOperator, Operator1, Operator2, OperatorWithNumericOperands, \
    BinaryOperator, EqualsOperator, NotEqualsOperator
from fmsd.expression.types import BinaryExpression, NumericExpression


class Negate(OperatorWithNumericOperands, Operator1, NumericOperator):
    DELIM = "-"


class Plus(OperatorWithNumericOperands, Operator2, NumericOperator):
    DELIM = "+"


class Minus(OperatorWithNumericOperands, Operator2, NumericOperator):
    DELIM = "-"


class Multiply(OperatorWithNumericOperands, Operator2, NumericOperator):
    DELIM = "×"


class DividedBy(OperatorWithNumericOperands, Operator2, NumericOperator):
    DELIM = "/"


class Power(OperatorWithNumericOperands, Operator2, NumericOperator):
    DELIM = "^"


class Max(OperatorWithNumericOperands, Operator2, NumericOperator):
    DELIM = "↑"


class Min(OperatorWithNumericOperands, Operator2, NumericOperator):
    DELIM = "↓"


class LessThan(OperatorWithNumericOperands, Operator2, BinaryOperator):
    DELIM = "<"


class LessThanOrEqualsTo(OperatorWithNumericOperands, Operator2, BinaryOperator):
    DELIM = "≤"


class GreaterThan(OperatorWithNumericOperands, Operator2, BinaryOperator):
    DELIM = ">"


class GreaterThanOrEqualsTo(OperatorWithNumericOperands, Operator2, BinaryOperator):
    DELIM = "≥"


class Equals(OperatorWithNumericOperands, Operator2, BinaryOperator, EqualsOperator):
    DELIM = "="


class NotEquals(OperatorWithNumericOperands, Operator2, BinaryOperator, NotEqualsOperator):
    DELIM = "⧧"


class Ternary(NumericOperator):
    def __init__(self, if_: Expression, then: Expression, else_: Expression) -> None:
        NumericOperator.__init__(self, if_, then, else_)
        assert isinstance(if_, BinaryExpression)
        assert isinstance(then, NumericExpression)
        assert isinstance(else_, NumericExpression)

    def __str__(self) -> str:
        return "if {} then {} else {} fi".format(*map(str, self.children))
