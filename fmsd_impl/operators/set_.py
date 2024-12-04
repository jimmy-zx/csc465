from fmsd.ast_ext.operator import Operator
from fmsd_impl.operators.props import Associative, Commutative, Idempotent


class Set(Operator):
    N = 1

    def print(self, depth: int) -> str:
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


class SetPower(Operator):
    N = 1
    DELIM = "ϟ"


class SetUnion(Operator, Commutative, Associative, Idempotent):
    N = 2
    DELIM = "∪"


class SetIntersect(Operator, Commutative, Associative, Idempotent):
    N = 2
    DELIM = "∩"


__all__ = [
    "Set",
    "Contents",
    "Size",
    "SetIn",
    "SubsetEq",
    "SetPower",
    "SetUnion",
    "SetIntersect",
]
