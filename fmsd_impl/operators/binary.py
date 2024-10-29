from fmsd.ast_ext.operator import Operator, Associative, Commutative


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
