from fmsd.ast_ext import Operator
from fmsd_impl.operators.props import Associative


class Join(Operator, Associative):
    N = 2
    DELIM = ";"


class Length(Operator):
    N = 1
    DELIM = "↔"


class Subscript(Operator, Associative):
    N = 2
    DELIM = "_"


class Duplicate(Operator):
    N = 2
    DELIM = "*"


class Star(Operator):
    N = 1
    DELIM = "*"


class Replace(Operator):
    N = 3

    def print(self, depth: int) -> str:
        return (
            f"{self.nodes[0].print(depth + 1)}"
            f"⊲{self.nodes[1].print(depth + 1)}⊳"
            f"{self.nodes[2].print(depth + 1)}"
        )


class StringRange(Operator):
    N = 2
    DELIM = ";.."


__all__ = [
    "Join",
    "Length",
    "Subscript",
    "Duplicate",
    "Star",
    "Replace",
    "StringRange",
]
