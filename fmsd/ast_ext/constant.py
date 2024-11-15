from typing import final

from fmsd.ast.node import Node


@final
class Constant(Node):
    def __init__(self, *args, **kwargs) -> None:
        if "name" in kwargs:
            assert len(kwargs) == 1
            name = kwargs["name"]
        elif len(args) == 1:
            name = args[0]
        else:
            assert False, "`name` is required for argument"
        super().__init__(name=name)

    def print(self, depth) -> str:
        return self.meta["name"]
