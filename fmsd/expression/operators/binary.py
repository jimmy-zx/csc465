from fmsd.expression import Expression
from fmsd.expression.operators import BinaryOperator, BinaryOperator2WithBinaryOperands
from fmsd.expression.types import BinaryExpression


class Flip(BinaryOperator):
    def __init__(self, operand: Expression) -> None:
        BinaryOperator.__init__(self, operand)
        assert isinstance(operand, BinaryExpression)

    @property
    def op(self) -> Expression:
        return self.operands[0]

    def __str__(self) -> str:
        return f"¬" + str(self.op)


class And(BinaryOperator2WithBinaryOperands):
    def __str__(self) -> str:
        return "({}∧{})".format(str(self.lhs), str(self.rhs))


class Or(BinaryOperator2WithBinaryOperands):
    def __str__(self) -> str:
        return "({}∨{})".format(str(self.lhs), str(self.rhs))


class Implies(BinaryOperator2WithBinaryOperands):
    def __str__(self) -> str:
        return "({}⇒{})".format(str(self.lhs), str(self.rhs))


class ImpliedBy(BinaryOperator2WithBinaryOperands):
    def __str__(self) -> str:
        return "({}⇐{})".format(str(self.lhs), str(self.rhs))


class Equals(BinaryOperator2WithBinaryOperands):
    def __str__(self) -> str:
        return "({}={})".format(str(self.lhs), str(self.rhs))


class NotEquals(BinaryOperator2WithBinaryOperands):
    def __str__(self) -> str:
        return "({}⧧{})".format(str(self.lhs), str(self.rhs))


class Ternary(BinaryOperator):
    def __init__(self, if_: Expression, then: Expression, else_: Expression) -> None:
        BinaryOperator.__init__(self, if_, then, else_)
        assert isinstance(if_, BinaryExpression)
        assert isinstance(then, BinaryExpression)
        assert isinstance(else_, BinaryExpression)

    def __str__(self) -> str:
        return "if {} then {} else {} fi".format(*map(str, self.operands))
