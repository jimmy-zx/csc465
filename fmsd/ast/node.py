from typing import Self, Iterator, final

from fmsd.ast.base import Base, CopyOnConstruction
from fmsd.utils.config import config

VarTable = dict[str, "Node"]


class Node(Base["Node"]):
    def __init__(self, *nodes: "Node") -> None:
        super().__init__()

        assert all(isinstance(node, Node) and node.parent is None for node in nodes)

        self.nodes = list(
            node if not node.copy_on_construction else node.copy() for node in nodes
        )
        self.parent: Node | None = None
        for node in self.nodes:
            node.parent = self

        for func in dir(self):
            if func.startswith("_init"):
                getattr(self, func)()

    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return False
        return self.nodes == other.nodes

    def __hash__(self):
        return hash((type(self), hash(tuple(self.nodes))))

    @final
    def __str__(self) -> str:
        return self.print(depth=config.max_level + 1)

    def print(self, depth: int = 0) -> str:
        return "Node(" + ", ".join(node.print(depth + 1) for node in self.nodes) + ")"

    def copy(self) -> Self:
        return type(self)(*(node.copy() for node in self.nodes))

    def variables(self) -> set[str]:
        return set().union(*(node.variables() for node in self.nodes))

    def eval(self, vt: VarTable) -> "Node":
        return type(self)(*(node.eval(vt) for node in self.nodes))

    def match(self, target: "Node", vt: VarTable) -> VarTable | None:
        if type(self) is not type(target):
            return None
        if len(self.nodes) != len(target.nodes):
            return None
        for lhs, rhs in zip(self.nodes, target.nodes):
            if (res := lhs.match(rhs, vt)) is None:
                return None
            vt = res
        return vt

    def get(self, index: list[int]) -> "Node":
        if not index:
            return self
        return self.nodes[index[0]].get(index[1:])

    def set(self, index: list[int], value: "Node") -> "Node":
        assert index
        if len(index) == 1:
            original = self.nodes[index[0]]
            assert value.parent is None
            if value.copy_on_construction:
                assert isinstance(value, Node)
                value = value.copy()
            self.nodes[index[0]] = value
            value.parent = self
            return original
        return self.nodes[index[0]].set(index[1:], value)

    def diff(self, other: "Node") -> list[int] | None:
        if self == other:
            return None
        if type(self) is not type(other):
            return []
        if not self.nodes:
            return []
        if len(self.nodes) != len(other.nodes):
            return []
        found = None
        for i, (lhs, rhs) in enumerate(zip(self.nodes, other.nodes)):
            if lhs != rhs:
                if found is not None:
                    return []
                found = i
        assert found is not None
        res = self.nodes[found].diff(other.nodes[found])
        assert res is not None
        return [found] + res

    def weak_diff(self, other: "Node") -> list[int] | None:
        if self == other:
            return None
        if type(self) is not type(other):
            return []
        if not self.nodes:
            return []
        if len(self.nodes) != len(other.nodes):
            return []
        for i, (lhs, rhs) in enumerate(zip(self.nodes, other.nodes)):
            if lhs != rhs:
                res = lhs.weak_diff(rhs)
                assert res is not None
                return [i] + res
        assert False

    def flatten(self) -> list["Node"]:
        nodes = []
        for node in self.nodes:
            if type(node) is type(self):
                nodes.extend(node.flatten())
            else:
                nodes.append(node)
        return nodes

    def context(self) -> list["Node"]:
        return self.parent.context() if self.parent is not None else []

    def validate(self) -> bool:
        return all(node.parent == self and node.validate() for node in self.nodes)

    def __iter__(self) -> Iterator["Node"]:
        return iter(self.nodes)

    def walk_preorder(self) -> Iterator["Node"]:
        yield self
        for node in self.nodes:
            yield from node.walk_preorder()


class Variable(Node, CopyOnConstruction):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash((type(self), self.name))

    def print(self, depth: int = 0) -> str:
        return self.name

    def copy(self) -> Self:
        return type(self)(self.name)

    def match(self, target: "Node", vt: VarTable) -> VarTable | None:
        if vt.get(self.name, target) != target:
            return None
        vt[self.name] = target
        return vt

    def eval(self, vt: VarTable) -> "Node":
        return vt.get(self.name, self).copy()

    def variables(self) -> set[str]:
        return {self.name}
