from fmsd.expression.constant import Constant
from fmsd.expression.types import Binary


class BinaryConstant(Constant, Binary):
    pass


TRUE = BinaryConstant("⊤")
FALSE = BinaryConstant("⊥")
