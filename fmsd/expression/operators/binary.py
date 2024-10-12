from fmsd.expression import Expression
from fmsd.expression.operators import BinaryOperator, Operator1, Operator2, OperatorWithBinaryOperands, \
    OperatorWithNumericOperands, EqualsOperator, NotEqualsOperator
from fmsd.expression.types import BinaryExpression


class Flip(OperatorWithBinaryOperands, Operator1, BinaryOperator):
    DELIM = "¬"


class And(OperatorWithBinaryOperands, Operator2, BinaryOperator):
    DELIM = "∧"


class Or(OperatorWithBinaryOperands, Operator2, BinaryOperator):
    DELIM = "∨"


class Implies(OperatorWithBinaryOperands, Operator2, BinaryOperator):
    DELIM = "⇒"


class ImpliedBy(OperatorWithBinaryOperands, Operator2, BinaryOperator):
    DELIM = "⇐"


class Equals(OperatorWithBinaryOperands, Operator2, BinaryOperator, EqualsOperator):
    DELIM = "="


class NotEquals(OperatorWithBinaryOperands, Operator2, BinaryOperator, NotEqualsOperator):
    DELIM = "⧧"


class Ternary(OperatorWithBinaryOperands, BinaryOperator):
    def __init__(self, if_: Expression, then: Expression, else_: Expression) -> None:
        OperatorWithBinaryOperands.__init__(self, if_, then, else_)

    def __str__(self) -> str:
        return "if {} then {} else {} fi".format(*map(str, self.children))
