from fmsd.ast_ext.operator import Operator
from fmsd.impl.operators import And, Implies
from fmsd_impl.operators.props import Associative, Commutative, Idempotent


class Flip(Operator):
    N = 1
    DELIM = "¬"


class Or(Operator, Associative, Commutative, Idempotent):
    N = 2
    DELIM = "∨"


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
