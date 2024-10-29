from fmsd.ast_ext.operator import Operator, Associative, Commutative


class Union(Operator, Associative, Commutative):
    N = 2
    DELIM = ","


class Intersect(Operator, Associative, Commutative):
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
