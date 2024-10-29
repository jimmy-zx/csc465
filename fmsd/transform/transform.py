from abc import ABC, abstractmethod
from typing import Callable

from fmsd.ast import Node


class Transform(ABC):
    def __init__(self) -> None:
        self.name: str | None = None

    @abstractmethod
    def verify(self, src: Node, dst: Node) -> bool: ...

    def __str__(self) -> str:
        if self.name is not None:
            return self.name
        return "<Transform>"

    def __repr__(self) -> str:
        return str(self)


class FunctionTransform(Transform):
    def __init__(self, func: Callable[[Node, Node], bool]) -> None:
        Transform.__init__(self)
        self.func = func

    def verify(self, src: Node, dst: Node) -> bool:
        return self.func(src, dst)

    def __eq__(self, other) -> bool:
        if not isinstance(other, FunctionTransform):
            return False
        return self.func == other.func
