from fmsd.expression.types import BinaryExpression, NumericExpression
from fmsd.expression import Variable


class BinaryVariable(Variable, BinaryExpression):
    pass


class NumericVariable(Variable, NumericExpression):
    pass