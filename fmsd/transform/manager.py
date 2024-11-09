import itertools
from abc import ABC, abstractmethod
from typing import Iterator

from fmsd.transform.transform import Transform


class TransformManager(ABC):
    @abstractmethod
    def __iter__(self) -> Iterator[Transform]: ...

    @abstractmethod
    def hit(self, transform: Transform, count: int) -> None: ...

    @abstractmethod
    def reset(self) -> None: ...


class ListTransformManager(TransformManager):
    def __init__(self, t_all: dict[str, Transform]) -> None:
        self.t_all = t_all
        self.cache: set[Transform] = set()
        self._miss = 0
        self._hit = 0
        self._count = 0

    def __iter__(self) -> Iterator[Transform]:
        return itertools.chain(self.cache, self.t_all.values())

    def hit(self, transform: Transform, count: int) -> None:
        self._count += count
        if transform in self.cache:
            self._hit += 1
        else:
            self._miss += 1
        self.cache.add(transform)

    def reset(self) -> None:
        self.cache = set()

    def __str__(self) -> str:
        return (
            "<ListTransformManager, "
            f"hit rate={self._hit / (self._hit + self._miss)}, "
            f"avg count={self._count / (self._hit + self._miss)}, "
            f"cache size={len(self.cache)}"
            ">"
        )
