from fmsd.expression import Expression
from fmsd.expression.operator import Operator
from fmsd.expression.operators import Operator2, OperatorWithSameOp1AndReturnType
from fmsd.expression.types import Type


class Context(Operator2, OperatorWithSameOp1AndReturnType):
    DELIM = ""

    def __str__(self) -> str:
        return "Context({},{})".format(*map(str, self.children))

    def context(self, index: list[int]) -> list["Expression"]:
        res = []
        if index:
            res.append(self.rhs)
            res.extend(self.children[index[0]].context(index[1:]))
        return res