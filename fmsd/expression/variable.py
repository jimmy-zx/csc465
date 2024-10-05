from fmsd.expression import Expression


class Variable(Expression):
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other) -> bool:
        if isinstance(other, Variable):
            if self.name == other.name:
                return True
        return False

    def eval_var(self, table: dict[str, "Expression"]) -> "Expression":
        return table.get(self.name, self).copy()

    def __str__(self) -> str:
        return self.name