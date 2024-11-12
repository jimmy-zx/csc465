from typing import Any, Final, Iterator, final

from fmsd.ast.base import Base, CopyOnConstruction
from fmsd.utils.config import config

VarTable = dict["Node", "Node"]


class Node(Base["Node"]):
    def __init__(self, *nodes: "Node", **meta) -> None:
        super().__init__()

        assert all(isinstance(node, Node) and node.parent is None for node in nodes)

        if nodes:
            decls = set.union(*(node.sym_decls() for node in nodes))
            for node in nodes:
                assert not decls.intersection(node.sym_refs() - node.sym_decls())

        self.meta: Final[dict] = meta
        self.nodes: Final[tuple[Node, ...]] = tuple(
            node if not node.copy_on_construction else node.copy() for node in nodes
        )
        self.parent: Node | None = None
        for node in self.nodes:
            node.parent = self

        for func in dir(self):
            if func.startswith("_init"):
                getattr(self, func)()

        self._cache: dict[str, Any] = {}

    def __getattribute__(self, item: str):
        attr = object.__getattribute__(self, item)
        if item in (
            "__hash__",
            "__str__",
            "variables",
            "sym_decls",
            "sym_refs",
        ):

            def wrapper():
                if item in self._cache:
                    return self._cache[item]
                self._cache[item] = (res := attr())
                return res

            return wrapper
        return attr

    @final
    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return False
        return self.nodes == other.nodes and self.meta == other.meta

    @final
    def __hash__(self):
        return hash((type(self), tuple(self.nodes), tuple(sorted(self.meta.items()))))

    @final
    def __str__(self) -> str:
        return self.print(depth=config.max_level + 1)

    def print(self, depth) -> str:
        return "Node(" + ", ".join(node.print(depth + 1) for node in self.nodes) + ")"

    @final
    def copy(self, copy_on_construction: bool = True) -> "Node":
        res = type(self)(*(node.copy() for node in self.nodes), **self.meta)
        res.copy_on_construction = res.copy_on_construction or copy_on_construction
        return res

    def variables(self) -> set["Node"]:
        return set().union(*(node.variables() for node in self.nodes))

    def eval(self, vt: VarTable) -> "Node":
        return type(self)(*(node.eval(vt) for node in self.nodes), **self.meta)

    def match(self, target: "Node", vt: VarTable) -> VarTable | None:
        if type(self) is not type(target):
            return None
        if self.meta != target.meta:
            return None
        if len(self.nodes) != len(target.nodes):
            return None
        for lhs, rhs in zip(self.nodes, target.nodes):
            if (res := lhs.match(rhs, vt)) is None:
                return None
            vt = res
        return vt

    @final
    def get(self, index: list[int]) -> "Node":
        if not index:
            return self
        return self.nodes[index[0]].get(index[1:])

    @final
    def replace(self, index: list[int], value: "Node") -> "Node":
        if not index:
            return value.copy() if value.copy_on_construction else value
        nodes = [node.copy() for node in self.nodes]
        nodes[index[0]] = nodes[index[0]].replace(index[1:], value)
        return type(self)(*nodes, **self.meta)

    @final
    def diff(self, other: "Node") -> list[int] | None:
        if self == other:
            return None
        if type(self) is not type(other):
            return []
        if self.meta != other.meta:
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

    @final
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

    @final
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

    @final
    def walk_preorder(self) -> Iterator["Node"]:
        yield self
        for node in self.nodes:
            yield from node.walk_preorder()

    def sym_decls(self) -> set["Node"]:
        return set().union(*(node.sym_decls() for node in self.nodes))

    def sym_refs(self) -> set["Node"]:
        return set().union(*(node.sym_refs() for node in self.nodes))


@final
class VarNode(Node, CopyOnConstruction):
    def __init__(self, *args, **kwargs) -> None:
        if "name" in kwargs:
            assert len(kwargs) == 1
            name = kwargs["name"]
        elif len(args) == 1:
            name = args[0]
        else:
            assert False, "`name` is required for argument"
        super().__init__(name=name)

    def print(self, depth: int) -> str:
        return self.meta["name"]

    def match(self, target: "Node", vt: VarTable) -> VarTable | None:
        if vt.get(self, target) != target:
            return None
        vt[self] = target
        return vt

    def eval(self, vt: VarTable) -> "Node":
        return vt.get(self, self).copy()

    def variables(self) -> set[Node]:
        return {self}

    def sym_refs(self) -> set["Node"]:
        return {self}
