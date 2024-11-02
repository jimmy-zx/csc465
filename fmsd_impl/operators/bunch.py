from fmsd.ast_ext.operator import Operator
from fmsd_impl.operators.props import Associative, Commutative, Idempotent


class Union(Operator, Associative, Commutative, Idempotent):
    N = 2
    DELIM = ","


class Intersect(Operator, Associative, Commutative, Idempotent):
    N = 2
    DELIM = "‘"


class In(Operator):
    N = 2
    DELIM = ":"


class Includes(Operator):
    N = 2
    DELIM = "::"


class BunchInterval(Operator):
    N = 2
    DELIM = ",.."


class Count(Operator):
    N = 1
    DELIM = "¢"


__all__ = [
    "Union",
    "Intersect",
    "In",
    "Includes",
    "BunchInterval",
    "Count",
]
