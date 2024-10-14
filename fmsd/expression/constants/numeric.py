from fmsd.expression.constant import Constant
from fmsd.expression.types import Numeric, Singular


class NumericConstant(Constant, Numeric, Singular):
    pass


INFINITY = NumericConstant("∞")
NEG_INFINITY = NumericConstant("-∞")

ZERO = NumericConstant("0")
ONE = NumericConstant("1")