from typing import Callable

from fmsd.expression import Expression, Variable
from fmsd.expression.constant import Constant


class Operator(Expression):
    def __init__(self, *operands: Expression) -> None:
        self.operands = list(operands)

    def copy(self) -> "Expression":
        return type(self)(*(op.copy() for op in self.operands))

    def eval_var(self, table: dict[str, "Expression"]) -> "Expression":
        return type(self)(*(op.eval_var(table) for op in self.operands))

    def variables(self) -> set[str]:
        vars = set()
        for op in self.operands:
            if isinstance(op, Variable):
                vars.add(op.name)
            elif isinstance(op, Operator):
                vars.update(op.variables())
        return vars

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

    def diff(self, other: "Expression", start: list[int] | None = None) -> list[int] | None:
        if not isinstance(other, Operator):
            return []
        if type(self) != type(other):
            return []
        start = start or [-1]
        start_idx = start[0]
        for i, (lhs, rhs) in enumerate(zip(self.operands, other.operands)):
            if i <= start_idx:
                continue
            if lhs != rhs:
                res = [i]
                res.extend(lhs.diff(rhs, start[1:]))
                return res
        return None

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