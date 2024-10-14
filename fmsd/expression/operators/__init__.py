from fmsd.expression import Expression
from fmsd.expression.operator import Operator
from fmsd.expression.types import Type


class Operator1(Operator):
    DELIM: str | None = None

    def _init_operator1(self) -> None:
        assert self.DELIM is not None
        assert len(self.children) == 1

    @property
    def op(self) -> Expression:
        return self.children[0]

    def __str__(self) -> str:
        return "{}{}".format(self.DELIM, self.op)


class Operator2(Operator):
    DELIM: str | None = None

    def _init_operator2(self) -> None:
        assert self.DELIM is not None
        assert len(self.children) == 2

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


class OperatorWithSameTypeOperands(Operator):
    def _init_operator_same_type_operands(self) -> None:
        assert len(set(op.type() for op in self.children)) == 1


class OperatorWithSameOp1AndReturnType(Operator):
    def type(self) -> Type:
        return self.children[0].type()


class OperatorWithBinaryOperands(OperatorWithSameTypeOperands):
    def _init_operator_binary_operands(self) -> None:
        assert all(op.type() == Type.BINARY for op in self.children)


class OperatorWithNumericOperands(OperatorWithSameTypeOperands):
    def _init_operator_numeric_operands(self) -> None:
        assert all(op.type() == Type.NUMERIC for op in self.children)


class OperatorWithSetOperands(OperatorWithSameTypeOperands):
    def _init_operator_numeric_operands(self) -> None:
        assert all(op.type() == Type.SET for op in self.children)


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
