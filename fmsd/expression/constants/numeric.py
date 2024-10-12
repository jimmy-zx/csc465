from fmsd.expression.constant import Constant
from fmsd.expression.types import NumericExpression


class NumericConstant(Constant, NumericExpression):
    pass


INFINITY = NumericConstant("∞")
NEG_INFINITY = NumericConstant("-∞")

ZERO = NumericConstant("0")
ONE = NumericConstant("1")