from fmsd.expression import Expression
from fmsd.expression.types import NumericExpression


class Bunch(Expression):
    pass


class NumericBunch(Bunch, NumericExpression):
    pass