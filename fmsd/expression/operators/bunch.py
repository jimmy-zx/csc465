from fmsd.expression.operators import Operator2, Operator1
from fmsd.expression.types import Binary, Numeric


class Union(Operator2):
    DELIM = ","


class Intersect(Operator2):
    DELIM = "‘"


class In(Operator2, Binary):
    DELIM = ":"


class Includes(Operator2, Binary):
    DELIM = "::"


class Count(Operator1, Numeric):
    DELIM = "¢"


