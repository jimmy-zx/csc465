from fmsd.ast_ext.operator import Operator


class Equals(Operator):
    N = 2
    DELIM = "="


class NotEquals(Operator):
    N = 2
    DELIM = "⧧"


class Ternary(Operator):
    N = 3

    def print(self, depth: int) -> str:
        return (
            f"if {self.nodes[0].print(depth + 1)} "
            f"then {self.nodes[1].print(depth + 1)} "
            f"else {self.nodes[2].print(depth + 1)} fi"
        )


__all__ = [
    "Equals",
    "NotEquals",
    "Ternary",
]
