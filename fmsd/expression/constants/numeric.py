from fmsd.expression.constant import Constant
from fmsd.expression.types import NumericExpression


class NumericConstant(Constant, NumericExpression):
    pass


INFINITY = NumericConstant("∞")
NEG_INFINITY = NumericConstant("-∞")


class Number(NumericConstant):
    def __init__(self, num: str) -> None:
        self.neg = False
        assert set(num).issubset(set("0123456789.-"))
        assert num.count(".") <= 1
        if (neg_count := num.count("-")) == 1:
            self.neg = True
            num = num[1:]
        else:
            assert neg_count == 0
        num = num.lstrip("0")
        if len(num) == 0:
            num = "0"
        Constant.__init__(self, num)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Number):
            return False
        return self.neg == other.neg and self.name == other.name


ZERO = Number("0")
ONE = Number("1")
