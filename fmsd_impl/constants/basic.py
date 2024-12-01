from fmsd.ast_ext.constant import Constant
from fmsd.impl.constants import FALSE, TRUE

ZERO = Constant("0")
ONE = Constant("1")
INFINITY = Constant("∞")

NULL = Constant("null")

NAT = Constant("nat")
INT = Constant("int")
RAT = Constant("rat")
REAL = Constant("real")
XINT = Constant("xint")
XREAL = Constant("xreal")

NIL = Constant("nil")

__all__ = [
    "TRUE",
    "FALSE",
    "ZERO",
    "ONE",
    "INFINITY",
    "NULL",
    "NAT",
    "INT",
    "RAT",
    "REAL",
    "XINT",
    "XREAL",
    "NIL",
]
