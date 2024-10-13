from fmsd.expression.constant import Constant
from fmsd.expression.types import Numeric


class NumericConstant(Constant, Numeric):
    pass


INFINITY = NumericConstant("∞")
NEG_INFINITY = NumericConstant("-∞")

ZERO = NumericConstant("0")
ONE = NumericConstant("1")