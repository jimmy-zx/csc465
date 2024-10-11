from fmsd.expression import Expression, Variable
from fmsd.expression.constant import Constant


class Operator(Expression):
    def __init__(self, *operands: Expression) -> None:
        Expression.__init__(self)
        self.children = list(operands)
        for child in self.children:
            child.parent = self

    def copy(self) -> "Expression":
        return type(self)(*(op.copy() for op in self.children))

    def eval_var(self, table: dict[str, "Expression"]) -> "Expression":
        return type(self)(*(op.eval_var(table) for op in self.children))

    def variables(self) -> set[str]:
        var_set = set()
        for op in self.children:
            if isinstance(op, Variable):
                var_set.add(op.name)
            elif isinstance(op, Operator):
                var_set.update(op.variables())
        return var_set

    def match(self, pattern: "Expression", matched: dict[str, "Expression"]) -> dict[str, "Expression"] | None:
        if isinstance(pattern, Variable):
            return Expression.match(self, pattern, matched)
        if not isinstance(pattern, Operator):
            return None
        if type(self) != type(pattern):
            return None
        for lhs, rhs in zip(self.children, pattern.children):
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
        for i, (lhs, rhs) in enumerate(zip(self.children, other.children)):
            if i <= start_idx:
                continue
            if lhs != rhs:
                res = [i]
                ext = lhs.diff(rhs, start[1:])
                assert ext is not None
                res.extend(ext)
                return res
        return None

    def is_constant(self) -> bool:
        return all(isinstance(op, Constant) for op in self.children)

    def get(self, index: list[int]) -> Expression:
        if not index:
            return self
        target = self.children[index[0]]
        next_index = index[1:]
        if not isinstance(target, Operator):
            assert not next_index
            return target
        return target.get(next_index)

    def set(self, index: list[int], repl: Expression) -> None:
        assert index
        next_index = index[1:]
        if not next_index:
            self.children[index[0]] = repl
            return
        target = self.children[index[0]]
        assert isinstance(target, Operator)
        return target.set(next_index, repl)

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.children == other.children