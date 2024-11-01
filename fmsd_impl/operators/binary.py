from fmsd.ast_ext.operator import Operator
from fmsd_impl.operators.props import Associative, Commutative


class Flip(Operator):
    N = 1
    DELIM = "¬"


class And(Operator, Associative, Commutative):
    N = 2
    DELIM = "∧"


class Or(Operator, Associative, Commutative):
    N = 2
    DELIM = "∨"


class Implies(Operator):
    N = 2
    DELIM = "⇒"


class ImpliedBy(Operator):
    N = 2
    DELIM = "⇐"


__all__ = [
    "Flip",
    "And",
    "Or",
    "Implies",
    "ImpliedBy",
]
