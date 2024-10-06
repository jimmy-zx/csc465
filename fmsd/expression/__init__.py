VarTable = dict[str, "Expression"]


class Expression:
    def copy(self) -> "Expression":
        return self

    def eval_var(self, table: VarTable) -> "Expression":
        return self

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

    def __eq__(self, other) -> bool:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return str(self)


class Variable(Expression):
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other) -> bool:
        if isinstance(other, Variable):
            if self.name == other.name:
                return True
        return False

    def eval_var(self, table: VarTable) -> "Expression":
        return table.get(self.name, self)

    def __str__(self) -> str:
        return self.name
