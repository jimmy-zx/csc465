from fmsd.ast_ext.constant import Constant

TRUE = Constant("⊤")
FALSE = Constant("⊥")

ZERO = Constant("0")
ONE = Constant("1")
INFINITY = Constant("∞")

NULL = Constant("null")

NAT = Constant("nat")
XINT = Constant("xint")
XREAL = Constant("xreal")

__all__ = [
    "TRUE",
    "FALSE",
    "ZERO",
    "ONE",
    "INFINITY",
    "NULL",
    "NAT",
    "XINT",
    "XREAL",
]
