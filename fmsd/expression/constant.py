from fmsd.expression import Expression


class Constant(Expression):
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other) -> bool:
        if isinstance(other, Constant):
            if self.name == other.name:
                return True
        return False

    def __str__(self) -> str:
        return self.name
