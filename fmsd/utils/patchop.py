"""
Ref: https://github.com/sagemath/sage/issues/6245
"""
from typing import Callable, TypeVar, Generic

L = TypeVar("L")
R = TypeVar("R")
T = TypeVar("T")


class InfixOperator(Generic[L, R, T]):
    def __init__(self, func: Callable[[L, R], T], lhs: L = None, rhs: R = None) -> None:
        self.func = func
        self.lhs = lhs
        self.rhs = rhs

    def __matmul__(self, rhs: R) -> T | "InfixOperator[L, R, T]":
        assert rhs is not None
        if self.lhs is not None:
            return self.func(self.lhs, rhs)
        if self.rhs is not None:
            raise Exception("rhs already occupied")
        return InfixOperator(self.func, None, rhs)

    def __rmatmul__(self, lhs: L) -> T | "InfixOperator[L, R, T]":
        assert lhs is not None
        if self.rhs is not None:
            return self.func(lhs, self.rhs)
        if self.lhs is not None:
            raise Exception("lhs already occupied")
        return InfixOperator(self.func, lhs, None)


class PrefixOperator(Generic[L, T]):
    def __init__(self, func: Callable[[L], T]) -> None:
        self.func = func

    def __matmul__(self, rhs: R) -> T:
        assert rhs is not None
        return self.func(rhs)