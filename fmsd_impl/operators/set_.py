from fmsd.ast_ext.operator import Operator
from fmsd_impl.operators.props import Associative, Commutative


class Set(Operator):
    N = 1

    def print(self, depth: int = 0) -> str:
        return f"{{{self.nodes[0]}}}"


class Contents(Operator):
    N = 1
    DELIM = "~"


class Size(Operator):
    N = 1
    DELIM = "$"


class SetIn(Operator):
    N = 2
    DELIM = "∈"


class SubsetEq(Operator):
    N = 2
    DELIM = "⊆"


class Power(Operator):
    N = 1
    DELIM = "ϟ"


class SetUnion(Operator, Commutative, Associative):
    N = 2
    DELIM = "∪"


class SetIntersect(Operator, Commutative, Associative):
    DELIM = "∩"
