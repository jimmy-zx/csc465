from fmsd.expression.constant import Constant
from fmsd.expression.types import BinaryExpression


class BinaryConstant(Constant, BinaryExpression):
    pass


TRUE = BinaryConstant("⊤")
FALSE = BinaryConstant("⊥")
