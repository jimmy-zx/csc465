from fmsd.expression.operators import (
    Operator1,
    Operator2,
    OperatorWithSameTypeOperands,
    AssociativeOperator,
    CommutativeOperator,
)
from fmsd.expression.types import Type, Numeric, Binary


class Set(Operator1):
    DELIM = ""

    def __str__(self) -> str:
        return f"{{{self.op}}}"

    def type(self) -> Type:
        return Type.SET

    def content_type(self) -> Type:
        return self.op.type()


class Contents(Operator1):
    DELIM = "~"

    def _init_set_contents(self) -> None:
        assert self.op.type() == Type.SET

    def type(self) -> Type:
        return self.op.content_type()


class Size(Operator1, Numeric):
    DELIM = "$"

    def _init_set_size(self) -> None:
        assert self.op.type() == Type.SET


class In(Operator2, Binary):
    DELIM = "∈"

    def _init_set_in(self) -> None:
        assert self.rhs.type() == Type.SET
        assert self.lhs.type() == self.rhs.content_type()


class SubsetEq(OperatorWithSameTypeOperands, Operator2, Binary):
    DELIM = "⊆"

    def _init_set_subseteq(self) -> None:
        assert self.lhs.type() == Type.SET
        assert self.lhs.content_type() == self.rhs.content_type()


class Power(Operator1):
    DELIM = "ϟ"

    def type(self) -> Type:
        return Type.SET

    def content_type(self) -> Type:
        return self.op.type()


class Union(
    Operator2, OperatorWithSameTypeOperands, AssociativeOperator, CommutativeOperator
):
    DELIM = "∪"

    def _init_set_union(self) -> None:
        assert self.lhs.type() == Type.SET
        assert self.lhs.content_type() == self.rhs.content_type()

    def type(self) -> Type:
        return Type.SET

    def content_type(self) -> Type:
        return self.lhs.content_type()


class Intersect(
    Operator2, OperatorWithSameTypeOperands, AssociativeOperator, CommutativeOperator
):
    DELIM = "∩"

    def _init_set_union(self) -> None:
        assert self.lhs.type() == Type.SET
        assert self.lhs.content_type() == self.rhs.content_type()

    def type(self) -> Type:
        return Type.SET

    def content_type(self) -> Type:
        return self.lhs.content_type()
