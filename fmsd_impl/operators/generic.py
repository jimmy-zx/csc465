from fmsd.ast_ext.operator import Operator


class Equals(Operator):
    N = 2
    DELIM = "="


class NotEquals(Operator):
    N = 2
    DELIM = "⧧"


class Ternary(Operator):
    N = 3

    def print(self, depth: int = 0) -> str:
        return f"if {self.nodes[0]} then {self.nodes[1]} else {self.nodes[2]} fi"
