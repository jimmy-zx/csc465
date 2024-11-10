from fmsd.ast_ext import Operator


class List(Operator):
    N = 1

    def print(self, depth: int = 0) -> str:
        return "[{}]".format(self.nodes[0].print(depth + 1))


class ListCompose(Operator):
    N = 2
    DELIM = " "


class ListAt(Operator):
    N = 2
    DELIM = "@"


class ListContents(Operator):
    N = 1
    DELIM = "~"


class ListJoin(Operator):
    N = 2
    DELIM = ";;"


class ListLength(Operator):
    N = 1
    DELIM = "#"


class ListDomain(Operator):
    N = 1
    DELIM = "☐"


class ListReplace(Operator):
    N = 3

    def print(self, depth: int = 0) -> str:
        return "{}→{}|{}".format(*[node.print(depth + 1) for node in self.nodes])


__all__ = [
    "List",
    "ListCompose",
    "ListContents",
    "ListJoin",
    "ListLength",
    "ListDomain",
    "ListReplace",
    "ListAt",
]
