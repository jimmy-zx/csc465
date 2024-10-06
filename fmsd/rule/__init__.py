from abc import ABC, abstractmethod
from typing import Callable

from fmsd.expression import Expression, VarTable


class Rule(ABC):
    @abstractmethod
    def __call__(self, exp: Expression, table: VarTable | None = None) -> Expression:
        ...


class MatchRule(Rule):
    def __init__(self, pattern: Expression, repl: Expression, equiv: bool = True) -> None:
        self.pattern = pattern
        self.repl = repl
        self.equiv = equiv
        # assert repl.variables().issubset(pattern.variables())

    def __call__(self, exp: Expression, table: VarTable | None = None, rev: bool = False) -> Expression:
        table = table or {}
        if not rev and (m := exp.match(self.pattern, table)) is not None:
            assert self.pattern.variables().issubset(m)
            assert self.repl.variables().issubset(m)
            return self.repl.eval_var(m)
        if self.equiv and (m := exp.match(self.repl, table)) is not None:
            assert self.pattern.variables().issubset(m)
            assert self.repl.variables().issubset(m)
            return self.pattern.eval_var(m)
        assert False

    def __repr__(self) -> str:
        if self.equiv:
            return str(self.pattern) + " === " + str(self.repl)
        else:
            return str(self.pattern) + " ==> " + str(self.repl)


class FunctionRule(Rule):
    def __init__(self, func: Callable[[Expression, VarTable | None], Expression]) -> None:
        self.func = func

    def __call__(self, exp: Expression, table: VarTable | None = None) -> Expression:
        table = table or {}
        return self.func(exp, table)