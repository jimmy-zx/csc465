from fmsd.expression import Expression
from fmsd.expression.operator import Operator
from fmsd.expression.types import BinaryExpression, NumericExpression


class BinaryOperator(Operator, BinaryExpression):
    pass


class NumericOperator(Operator, NumericExpression):
    pass


class Operator1(Operator):
    DELIM: str | None = None

    def __init__(self, op: Expression) -> None:
        assert self.DELIM is not None
        Operator.__init__(self, op)

    @property
    def op(self) -> Expression:
        return self.children[0]

    def __str__(self) -> str:
        return "{}{}".format(self.DELIM, self.op)


class Operator2(Operator):
    DELIM: str | None = None

    def __init__(self, lhs: Expression, rhs: Expression) -> None:
        assert self.DELIM is not None
        Operator.__init__(self, lhs, rhs)

    @property
    def lhs(self) -> Expression:
        return self.children[0]

    @property
    def rhs(self) -> Expression:
        return self.children[1]

    def __str__(self) -> str:
        return "({}{}{})".format(
            str(self.lhs), self.DELIM, str(self.rhs)
        )


class OperatorWithBinaryOperands(Operator):
    def __init__(self, *operands: Expression) -> None:
        for op in operands:
            assert isinstance(op, BinaryExpression)
        Operator.__init__(self, *operands)


class OperatorWithNumericOperands(Operator):
    def __init__(self, *operands: Expression) -> None:
        for op in operands:
            assert isinstance(op, NumericExpression)
        Operator.__init__(self, *operands)


class EqualsOperator(Operator):
    pass


class NotEqualsOperator(Operator):
    pass


class AssociativeOperator(Operator):
    def collect(self) -> list["Expression"]:
        ops = []
        for op in self.children:
            if type(self) == type(op):
                ops.extend(op.collect())
            else:
                ops.append(op)
        return ops


class CommutativeOperator(Operator):
    pass

