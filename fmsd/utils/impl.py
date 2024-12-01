from abc import ABC, abstractmethod

from fmsd.transform import TransformManager


class Implementation(ABC):
    @abstractmethod
    def transform_manager(self) -> TransformManager: ...


impl: Implementation | None = None
