from typing import Generic, Self, TypeVar

from fmsd.utils.config import config

T = TypeVar("T")


class Base(Generic[T]):
    def __init__(self) -> None:
        self.stack = config.get_trace()
        self.copy_on_construction = False

    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return False
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()

    def __repr__(self):
        return str(self)

    def __invert__(self) -> T:
        raise NotImplementedError()

    def __and__(self, other: T) -> T:
        raise NotImplementedError()

    def __or__(self, other: T) -> T:
        raise NotImplementedError()

    def __rshift__(self, other: T) -> T:
        raise NotImplementedError()

    def __lshift__(self, other: T) -> T:
        raise NotImplementedError()

    def __neg__(self) -> T:
        raise NotImplementedError()

    def __add__(self, other: T) -> T:
        raise NotImplementedError()

    def __sub__(self, other: T) -> T:
        raise NotImplementedError()

    def __mul__(self, other: T) -> T:
        raise NotImplementedError()

    def __truediv__(self, other: T) -> T:
        raise NotImplementedError()

    def __pow__(self, power: T) -> T:
        raise NotImplementedError()

    def __lt__(self, other: T) -> T:
        raise NotImplementedError()

    def __le__(self, other: T) -> T:
        raise NotImplementedError()

    def __gt__(self, other: T) -> T:
        raise NotImplementedError()

    def __ge__(self, other: T) -> T:
        raise NotImplementedError()

    def __matmul__(self, other):
        return NotImplemented

    def copy(self) -> Self:
        return self


class CopyOnConstruction:
    def __init__(self) -> None:
        self.copy_on_construction = False

    def _init_copy_on_construction(self):
        self.copy_on_construction = True
