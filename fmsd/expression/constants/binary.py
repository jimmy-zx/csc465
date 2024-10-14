from fmsd.expression.constant import Constant
from fmsd.expression.types import Binary, Singular


class BinaryConstant(Constant, Binary, Singular):
    pass


TRUE = BinaryConstant("⊤")
FALSE = BinaryConstant("⊥")
