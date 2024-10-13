from enum import Enum


class Type(Enum):
    BINARY = 0
    NUMERIC = 1


class Typed:
    def type(self) -> Type:
        raise NotImplementedError()

    def singular(self) -> bool:
        return False


class Binary(Typed):
    def type(self) -> Type:
        return Type.BINARY


class Numeric(Typed):
    def type(self) -> Type:
        return Type.NUMERIC
