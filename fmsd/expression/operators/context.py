from fmsd.expression import Expression
from fmsd.expression.operators import Operator2, OperatorWithSameOp1AndReturnType


class Context(Operator2, OperatorWithSameOp1AndReturnType):
    DELIM = ""

    def __str__(self) -> str:
        return f"Context({self.lhs}, {self.rhs})"

    def context(self, index: list[int]) -> list["Expression"]:
        res = []
        if index:
            res.append(self.rhs)
            res.extend(self.children[index[0]].context(index[1:]))
        return res
