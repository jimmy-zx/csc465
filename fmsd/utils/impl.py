from abc import ABC, abstractmethod

from fmsd.ast.node import Node
from fmsd.transform import Transform


class Implementation(ABC):
    @abstractmethod
    def node_to_transform(self, node: Node) -> Transform: ...

    @abstractmethod
    def t_all(self) -> dict[str, Transform]: ...


impl: Implementation | None = None
