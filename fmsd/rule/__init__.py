import warnings
from abc import ABC, abstractmethod
from typing import Callable

from fmsd.expression import Expression, VarTable
from fmsd.expression.operators.binary import Implies
from fmsd.expression.operators.generic import Equals

warnings.warn("This module is deprecated", DeprecationWarning)


class Rule(ABC):
    def __init__(self, name: str = "") -> None:
        self.name = name

    @abstractmethod
    def __call__(self, exp: Expression, table: VarTable | None = None) -> Expression:
        ...


class MatchRule(Rule):
    def __init__(self, pattern: Expression, repl: Expression, equiv: bool = True, name: str = "") -> None:
        assert isinstance(pattern, Expression)
        assert isinstance(repl, Expression)
        Rule.__init__(self, name)
        self.pattern = pattern
        self.repl = repl
        self.equiv = equiv
        # assert repl.variables().issubset(pattern.variables())

    def __call__(self, exp: Expression, table: VarTable | None = None, rev: bool = False) -> Expression:
        table_cpy = table.copy() if table else {}
        if not rev and (m := exp.match(self.pattern, table_cpy)) is not None:
            assert self.pattern.variables().issubset(m)
            assert self.repl.variables().issubset(m)
            return self.repl.eval_var(m)
        table_cpy = table.copy() if table else {}
        if self.equiv and (m := exp.match(self.repl, table_cpy)) is not None:
            assert self.pattern.variables().issubset(m)
            assert self.repl.variables().issubset(m)
            return self.pattern.eval_var(m)
        assert False

    def to_expr(self) -> Expression:
        if self.equiv:
            return Equals(self.pattern, self.repl)
        return Implies(self.pattern, self.repl)

    def __repr__(self) -> str:
        if self.equiv:
            return str(self.pattern) + " === " + str(self.repl)
        else:
            return str(self.pattern) + " ==> " + str(self.repl)


class FunctionRule(Rule):
    def __init__(self, func: Callable[[Expression, VarTable | None], Expression], name: str = "") -> None:
        Rule.__init__(self, name)
        self.func = func

    def __call__(self, exp: Expression, table: VarTable | None = None) -> Expression:
        table = table or {}
        return self.func(exp, table)
