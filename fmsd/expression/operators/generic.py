from fmsd.expression import Expression
from fmsd.expression.operator import Operator
from fmsd.expression.operators import Operator2, AssociativeOperator, CommutativeOperator, OperatorWithSameTypeOperands
from fmsd.expression.types import Binary, Type


class Equals(OperatorWithSameTypeOperands, Operator2, Binary, AssociativeOperator,
             CommutativeOperator):
    DELIM = "="


class NotEquals(OperatorWithSameTypeOperands, Operator2, Binary):
    DELIM = "⧧"


class Ternary(Operator):
    def __init__(self, if_: Expression, then: Expression, else_: Expression) -> None:
        assert if_.type() == Type.BINARY
        assert then.type() == else_.type()
        Operator.__init__(self, if_, then, else_)

    def type(self) -> Type:
        return self.children[1].type()

    def __str__(self) -> str:
        return "if {} then {} else {} fi".format(*map(str, self.children))
