from fmsd.ast_ext.operator import Operator, Associative, Commutative


class Negate(Operator):
    N = 1
    DELIM = "-"


class Plus(Operator, Commutative, Associative):
    N =  2
    DELIM = "+"


class Minus(Operator):
    N = 2
    DELIM = "-"


class Multiply(Operator, Commutative, Associative):
    N = 2
    DELIM = "×"


class DividedBy(Operator):
    N = 2
    DELIM = "/"


class Power(Operator):
    N = 2
    DELIM = "^"


class Max(Operator, Commutative, Associative):
    N = 2
    DELIM = "↑"


class Min(Operator, Commutative, Associative):
    N = 2
    DELIM = "↓"


class LessThan(Operator):
    N = 2
    DELIM = "<"


class LessThanOrEqualsTo(Operator):
    N = 2
    DELIM = "≤"


class GreaterThan(Operator):
    N = 2
    DELIM = ">"


class GreaterThanOrEqualsTo(Operator):
    N = 2
    DELIM = "≥"
