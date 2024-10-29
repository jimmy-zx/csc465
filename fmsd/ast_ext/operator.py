from fmsd.ast.node import Node
from fmsd.utils.config import config


class Operator(Node):
    N: int | None = None
    DELIM: str | None = None

    def _init_operator(self) -> None:
        if self.N is not None:
            assert len(self.nodes) == self.N

    def print(self, depth: int = 0) -> str:
        assert self.DELIM is not None
        if self.N == 1:
            return f"{self.DELIM}{self.nodes[0].print(depth + 1)}"
        if self.N == 2:
            return (
                config.truecolor(depth, "(")
                + f"{self.nodes[0].print(depth + 1)}{self.DELIM}{self.nodes[1].print(depth + 1)}"
                + config.truecolor(depth, ")")
            )
        assert False


class Associative(Node):
    pass


class Commutative(Node):
    pass
