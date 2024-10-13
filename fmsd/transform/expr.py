from fmsd.expression import Expression
from fmsd.expression.constants.binary import TRUE
from fmsd.expression.operators.binary import Implies
from fmsd.expression.operators.generic import Equals
from fmsd.transform import Transform


class ExpressionTransform(Transform):
    def __init__(self, expr: Expression, name: str) -> None:
        Transform.__init__(self)
        self.name = name
        self.expr = expr

    def verify(self, src: Expression, dst: Expression) -> bool:
        if dst == TRUE and src.match(self.expr, {}) is not None:
            return True
        if src == TRUE and dst.match(self.expr, {}) is not None:
            return True
        if isinstance(self.expr, (Equals, Implies)):
            if (m := src.match(self.expr.lhs, {})) is not None:
                if dst.match(self.expr.rhs, m) == m:
                    return True
        if isinstance(self.expr, Equals):
            if (m := src.match(self.expr.rhs, {})) is not None:
                if dst.match(self.expr.lhs, m) == m:
                    return True
