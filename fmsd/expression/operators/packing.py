from fmsd.expression import Expression
from fmsd.expression.operators import Operator1
from fmsd.expression.structure import Bunch, String


class Set(Operator1):
    def __init__(self, op: Expression) -> None:
        assert isinstance(op, Bunch)
        Operator1.__init__(self, op)

    def __str__(self) -> str:
        return "{" + str(self.op) + "}"


class List(Operator1):
    def __init__(self, op: Expression) -> None:
        assert isinstance(op, String)
        Operator1.__init__(self, op)

    def __str__(self) -> str:
        return "[" + str(self.op) + "]"
