VarTable = dict[str, "Expression"]


class Expression:
    def __init__(self) -> None:
        self.parent: Expression | None = None
        self.children: list[Expression] = []

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

    def is_constant(self) -> bool:
        raise NotImplementedError()

    def get(self, index: list[int]) -> "Expression":
        raise NotImplementedError()

    def set(self, index: list[int], repl: "Expression") -> None:
        raise NotImplementedError()

    def diff(self, other: "Expression", start: list[int] | None = None) -> list[int] | None:
        raise NotImplementedError()

    def diff_all(self, other: "Expression") -> list[list[int]]:
        diff = self.diff(other)
        if diff is None:
            return []
        diffs = [diff]
        while (diff := self.diff(other, diffs[-1])) is not None:
            diffs.append(diff)
        return diffs


class Variable(Expression):
    def __hash__(self):
        return hash(self.name)

    def __init__(self, name: str) -> None:
        Expression.__init__(self)
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
