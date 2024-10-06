from abc import ABC, abstractmethod
from typing import Callable

from fmsd.expression import Expression


class Rule(ABC):
    @abstractmethod
    def apply(self, exp: Expression) -> Expression:
        ...


class MatchRule(Rule):
    def __init__(self, pattern: Expression, repl: Expression, equiv: bool = False) -> None:
        self.pattern = pattern
        self.repl = repl
        self.equiv = equiv

    def apply(self, exp: Expression) -> Expression:
        if m := exp.match(self.pattern, {}) is not None:
            return self.repl.eval_var(m)
        if self.equiv and (m := exp.match(self.repl, {})) is not None:
            return self.pattern.eval_var(m)


class FunctionRule(Rule):
    def __init__(self, func: Callable[[Expression, ], Expression]) -> None:
        self.func = func

    def apply(self, exp: Expression) -> Expression:
        return self.func(exp)