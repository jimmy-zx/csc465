VarTable = dict[str, "Expression"]


class Expression:
    def __eq__(self, other) -> bool:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return str(self)

    def copy(self) -> "Expression":
        return self

    def eval_var(self, table: VarTable) -> "Expression":
        return self

    def variables(self) -> set[str]:
        return set()

    def match(self, pattern: "Expression", matched: VarTable) -> VarTable | None:
        if isinstance(pattern, Variable):
            if pattern.name in matched:
                if self != matched[pattern.name]:
                    return None
            else:
                matched[pattern.name] = self
            return matched
        if self == pattern:
            return matched
        return None

    def diff(self, other: "Expression", start: list[int] | None = None) -> list[int] | None:
        raise NotImplementedError()


class Variable(Expression):
    def __hash__(self):
        return hash(self.name)

    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other) -> bool:
        if isinstance(other, Variable):
            if self.name == other.name:
                return True
        return False

    def __str__(self) -> str:
        return self.name

    def eval_var(self, table: VarTable) -> "Expression":
        return table.get(self.name, self)

    def diff(self, other: "Expression", start: list[int] | None = None) -> list[int] | None:
        if not isinstance(other, Variable):
            return []
        if type(self) != type(other):
            return []
        if self == other:
            return None
        return []

