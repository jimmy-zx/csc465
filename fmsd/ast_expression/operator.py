from fmsd.ast.node import Node


class Operator(Node):
    N: int | None = None
    DELIM: str | None = None

    def _init_operator(self) -> None:
        if self.N is not None:
            assert len(self.nodes) == self.N

    def __str__(self) -> str:
        assert self.DELIM is not None
        if self.N == 1:
            return f"{self.DELIM}({self.nodes[0]})"
        if self.N == 2:
            return f"({self.nodes[0]}){self.DELIM}({self.nodes[1]})"
        assert False


class Associative:
    pass


class Commutative:
    pass
