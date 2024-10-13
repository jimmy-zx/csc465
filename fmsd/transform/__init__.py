from abc import ABC, abstractmethod

from fmsd.expression import Expression


class Transform(ABC):
    def __init__(self) -> None:
        self.name: str | None = None

    @abstractmethod
    def verify(self, src: Expression, dst: Expression) -> bool:
        ...
