from fmsd.expression.constant import Constant
from fmsd.expression.types import Numeric


class NumericBunchConstant(Constant, Numeric):
    def singular(self) -> bool:
        return False


NULL = NumericBunchConstant("null")

NAT = NumericBunchConstant("nat")

XINT = NumericBunchConstant("xint")

XREAL = NumericBunchConstant("xreal")
