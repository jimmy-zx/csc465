from typing import Callable

from fmsd.expression import Expression, Variable
from fmsd.expression.constant import Constant


class Operator(Expression):
    def __init__(self, *operands: Expression) -> None:
        self.operands = list(operands)

    def copy(self) -> "Expression":
        return type(self)(*self.operands)

    def eval_var(self, table: dict[str, "Expression"]) -> "Expression":
        return type(self)(*(op.eval_var(table) for op in self.operands))

    def match(self, pattern: "Expression", matched: dict[str, "Expression"]) -> dict[str, "Expression"] | None:
        if isinstance(pattern, Variable):
            return Expression.match(self, pattern, matched)
        if not isinstance(pattern, Operator):
            return None
        if type(self) != type(pattern):
            return None
        for lhs, rhs in zip(self.operands, pattern.operands):
            if (res := lhs.match(rhs, matched)) is None:
                return None
            matched = res
        return matched

    def is_constant(self) -> bool:
        return all(isinstance(op, Constant) for op in self.operands)

    def get(self, index: list[int]) -> Expression:
        if not index:
            return self
        target = self.operands[index[0]]
        next_index = index[1:]
        if not isinstance(target, Operator):
            assert not next_index
            return target
        return target.get(next_index)

    def set(self, index: list[int], repl: Expression) -> None:
        assert index
        next_index = index[1:]
        if not next_index:
            self.operands[index[0]] = repl
            return
        target = self.operands[index[0]]
        assert isinstance(target, Operator)
        return target.set(next_index, repl)

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.operands == other.operands