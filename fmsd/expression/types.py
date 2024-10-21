from enum import Enum


class Type(Enum):
    ANY = 0
    BINARY = 1
    NUMERIC = 2
    SET = 3

    def match(self, other: "Type") -> bool:
        if self == self.ANY:
            return True
        return self == other


class Typed:
    def type(self) -> Type:
        raise NotImplementedError()

    def content_type(self) -> Type:
        raise NotImplementedError()

    def singular(self) -> bool:
        return False


class Binary(Typed):
    def type(self) -> Type:
        return Type.BINARY


class Numeric(Typed):
    def type(self) -> Type:
        return Type.NUMERIC


class Singular(Typed):
    def singular(self) -> bool:
        return True
