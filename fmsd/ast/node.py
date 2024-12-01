from typing import Callable, Final, Iterator, final

from fmsd.ast.base import Base
from fmsd.utils.config import config

VarTable = dict["Node", "Node"]


class Node(Base["Node"]):
    # Defined in fmsd.ast_ext.variable
    _init_symbols: Callable[["Node"], None] | None = None

    def __init__(self, *nodes: "Node", **meta) -> None:
        super().__init__()

        assert all(isinstance(node, Node) for node in nodes)

        self.meta: Final[dict] = meta
        self.nodes: Final[tuple[Node, ...]] = tuple(nodes)

        for func in dir(self):
            if func.startswith("_init"):
                getattr(self, func)()

        self._hash_cache: int = self._hash()

    @final
    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return False
        return self.nodes == other.nodes and self.meta == other.meta

    @final
    def _hash(self) -> int:
        return hash((type(self), tuple(self.nodes), tuple(sorted(self.meta.items()))))

    @final
    def __hash__(self):
        return self._hash_cache

    @final
    def __str__(self) -> str:
        return self.print(depth=config.max_level + 1)

    def print(self, depth) -> str:
        return "Node(" + ", ".join(node.print(depth + 1) for node in self.nodes) + ")"

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
            return value
        nodes = list(self.nodes)
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

    @final
    def walk_preorder(self) -> Iterator["Node"]:
        yield self
        for node in self.nodes:
            yield from node.walk_preorder()

    def sym_decls(self) -> set["Node"]:
        return set().union(*(node.sym_decls() for node in self.nodes))


@final
class VarNode(Node):
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
        return vt.get(self, self)

    @staticmethod
    def varnodes(node: Node) -> set[Node]:
        if isinstance(node, VarNode):
            return {node}
        return set().union(*(VarNode.varnodes(node) for node in node.nodes))
