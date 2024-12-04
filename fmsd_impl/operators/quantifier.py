from abc import ABC
from typing import Self

from fmsd.ast import Node
from fmsd.ast_ext import Operator
from fmsd_impl.operators.function import Function


class Quantifier(Operator, ABC):

    def _init_quantifier(self) -> None:
        assert type(self) is not Quantifier

    @classmethod
    def from_func(cls, *nodes: Node, **meta) -> Self:
        return cls(Function(*nodes), **meta)

    @classmethod
    def from_list(cls, vars_: list[tuple[Node, Node]], expr: Node) -> Node:
        if not vars_:
            return expr
        return cls.from_func(*vars_[0], cls.from_list(vars_[1:], expr))

    @staticmethod
    def from_chain(
        vars_: list[tuple[type["Quantifier"], Node, Node]], expr: Node
    ) -> Node:
        if not vars_:
            return expr
        return vars_[0][0].from_func(
            *vars_[0][1:], Quantifier.from_chain(vars_[1:], expr)
        )


class Forall(Quantifier):
    N = 1
    DELIM = "∀"


class Exists(Quantifier):
    N = 1
    DELIM = "∃"


class Sum(Quantifier):
    N = 1
    DELIM = "Σ"


class Product(Quantifier):
    N = 1
    DELIM = "Π"


class QMax(Quantifier):
    N = 1
    DELIM = "⇑"


class QMin(Quantifier):
    N = 1
    DELIM = "⇓"


class Solution(Quantifier):
    N = 1
    DELIM = "§"


__all__ = [
    "Quantifier",
    "Forall",
    "Exists",
    "Sum",
    "Product",
    "QMax",
    "QMin",
    "Solution",
]
