from fmsd.expression import Expression


class Constant(Expression):
    def __init__(self, name: str) -> None:
        Expression.__init__(self)
        self.name = name

    def diff(self, other: "Expression", start: int = 0) -> list[int] | None:
        if start > 0:
            return None
        if self == other:
            return None
        return []

    def __eq__(self, other) -> bool:
        if not isinstance(other, Constant):
            return False
        if type(self) != type(other):
            return False
        if self.name != other.name:
            return False
        return True

    def __str__(self) -> str:
        return self.name
