from abc import ABC, abstractmethod

from fmsd.expression import Expression


class Transform(ABC):
    def __init__(self) -> None:
        self.name: str | None = None

    @abstractmethod
    def verify(self, src: Expression, dst: Expression) -> bool:
        ...

    def __str__(self) -> str:
        if self.name is not None:
            return self.name
        return "<Transform>"

    def __repr__(self) -> str:
        return str(self)
