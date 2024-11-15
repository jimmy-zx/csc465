from fmsd.ast_ext import Operator


class Forall(Operator):
    N = 1
    DELIM = "∀"


class Exists(Operator):
    N = 1
    DELIM = "∃"


class Sum(Operator):
    N = 1
    DELIM = "Σ"


class Product(Operator):
    N = 1
    DELIM = "Π"


class QMax(Operator):
    N = 1
    DELIM = "⇑"


class QMin(Operator):
    N = 1
    DELIM = "⇓"


class Solution(Operator):
    N = 1
    DELIM = "§"


__all__ = [
    "Forall",
    "Exists",
    "Sum",
    "Product",
    "QMax",
    "QMin",
    "Solution",
]
