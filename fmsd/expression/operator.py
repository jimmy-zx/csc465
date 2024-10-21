from fmsd.expression import Expression, Variable
from fmsd.expression.constant import Constant


class Operator(Expression):
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

    def match(self,
              pattern: "Expression",
              matched: dict[str, "Expression"]) -> dict[str, "Expression"] | None:
        if isinstance(pattern, Variable):
            return pattern.vmatch(self, matched)
        if not isinstance(pattern, Operator):
            return None
        if type(self) is not type(pattern):
            return None
        for lhs, rhs in zip(self.children, pattern.children):
            if (res := lhs.match(rhs, matched)) is None:
                return None
            matched = res
        return matched

    def diff(self, other: "Expression", start: int = 0) -> list[int] | None:
        """
        Returns the difference of two operator (tree)s

        Behavior:
        If self == other, returns None
        If start > 0, returns the diff along first different child
        If start <= 0, returns diff along the only different child, or the current node
        """
        if self == other:
            return None
        found: list[int] | None = None
        if start > 0:
            for i, (lhs, rhs) in enumerate(zip(self.children, other.children)):
                if lhs != rhs:
                    found = [i]
                    ext = lhs.diff(rhs, start - 1)
                    if ext is not None:
                        found.extend(ext)
                        return found
            return None
        if type(self) is not type(other):
            return []
        for i, (lhs, rhs) in enumerate(zip(self.children, other.children)):
            if lhs != rhs:
                if found:  # 1+ difference in operands, this is the root difference
                    return []
                found = [i]
                ext = lhs.diff(rhs, start - 1)
                assert ext is not None
                found.extend(ext)
        return found

    def is_constant(self) -> bool:
        return all(isinstance(op, Constant) for op in self.children)

    def context(self, index: list[int]) -> list["Expression"]:
        res = []
        if index:
            res.extend(self.children[index[0]].context(index[1:]))
        return res

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
        target.set(next_index, repl)

    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return False
        if self.type() != other.type():
            return False
        return self.children == other.children

    def __hash__(self) -> int:
        return hash((type(self), hash(tuple(self.children))))

    def singular(self) -> bool:
        return all(op.singular() for op in self.children)
