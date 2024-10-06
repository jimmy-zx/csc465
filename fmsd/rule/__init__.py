from abc import ABC, abstractmethod
from typing import Callable

from fmsd.expression import Expression, VarTable


class Rule(ABC):
    @abstractmethod
    def __call__(self, exp: Expression, table: VarTable | None = None) -> Expression:
        ...


class MatchRule(Rule):
    def __init__(self, pattern: Expression, repl: Expression, equiv: bool = False) -> None:
        self.pattern = pattern
        self.repl = repl
        self.equiv = equiv

    def __call__(self, exp: Expression, table: VarTable | None = None) -> Expression:
        table = table or {}
        if (m := exp.match(self.pattern, table)) is not None:
            return self.repl.eval_var(m)
        if self.equiv and (m := exp.match(self.repl, table)) is not None:
            return self.pattern.eval_var(m)
        assert False


class FunctionRule(Rule):
    def __init__(self, func: Callable[[Expression, VarTable | None], Expression]) -> None:
        self.func = func

    def __call__(self, exp: Expression, table: VarTable | None = None) -> Expression:
        table = table or {}
        return self.func(exp, table)