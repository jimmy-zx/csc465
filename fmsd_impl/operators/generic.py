from fmsd.ast_expression.operator import Operator


class Equals(Operator):
    N = 2
    DELIM = "="


class NotEquals(Operator):
    N = 2
    DELIM = "⧧"


class Ternary(Operator):
    N = 3

    def __str__(self) -> str:
        return (
            f"if {self.nodes[0]} then {self.nodes[1]} else {self.nodes[2]} fi"
        )
