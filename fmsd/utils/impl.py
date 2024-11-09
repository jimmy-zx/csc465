from abc import ABC, abstractmethod

from fmsd.ast.node import Node
from fmsd.transform import Transform, TransformManager


class Implementation(ABC):
    @abstractmethod
    def node_to_transform(self, node: Node) -> Transform: ...

    @abstractmethod
    def transform_manager(self) -> TransformManager: ...


impl: Implementation | None = None
