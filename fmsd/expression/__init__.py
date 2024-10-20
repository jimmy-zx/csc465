import fmsd.utils.config as config
from fmsd.expression.types import Typed
from fmsd.utils.trace import get_trace

VarTable = dict[str, "Expression"]


class ImportPatchException(Exception):
    def __init__(self):
        Exception.__init__(self, "import fmsd.utils.patch")


class Expression(Typed):
    def __init__(self, *children: "Expression", cfg: config.Config | None = None) -> None:
        self.config = cfg or config.config
        self.stack = get_trace() if self.config.trace else None
        self.parent: Expression | None = None
        self.children: list[Expression] = list(children)
        for child in self.children:
            child.parent = self

        for func in dir(self):
            if func.startswith("_init"):
                getattr(self, func)()

    def __eq__(self, other) -> bool:
        raise NotImplementedError()

    def __hash__(self) -> int:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return str(self)

    def copy(self) -> "Expression":
        return self

    def eval_var(self, table: VarTable) -> "Expression":
        return self

    def variables(self) -> set[str]:
        return set()

    def match(self, pattern: "Expression", matched: VarTable) -> VarTable | None:
        if isinstance(pattern, Variable):
            return pattern.vmatch(self, matched)
        if self == pattern:
            return matched
        return None

    def is_constant(self) -> bool:
        return False

    def context(self, index: list[int]) -> list["Expression"]:
        return []

    def get(self, index: list[int]) -> "Expression":
        if not index:
            return self
        raise NotImplementedError()

    def set(self, index: list[int], repl: "Expression") -> None:
        raise NotImplementedError()

    def diff(self, other: "Expression", start: int = 0) -> list[int] | None:
        raise NotImplementedError()

    def collect(self) -> list["Expression"]:
        return [self]

    def __invert__(self) -> "Expression":
        raise ImportPatchException()

    def __and__(self, other: "Expression") -> "Expression":
        raise ImportPatchException()

    def __or__(self, other: "Expression") -> "Expression":
        raise ImportPatchException()

    def __rshift__(self, other: "Expression") -> "Expression":
        raise ImportPatchException()

    def __lshift__(self, other: "Expression") -> "Expression":
        raise ImportPatchException()

    def __neg__(self) -> "Expression":
        raise ImportPatchException()

    def __add__(self, other: "Expression") -> "Expression":
        raise ImportPatchException()

    def __sub__(self, other: "Expression") -> "Expression":
        raise ImportPatchException()

    def __mul__(self, other: "Expression") -> "Expression":
        raise ImportPatchException()

    def __truediv__(self, other: "Expression") -> "Expression":
        raise ImportPatchException()

    def __pow__(self, power: "Expression") -> "Expression":
        raise ImportPatchException()

    def __lt__(self, other: "Expression") -> "Expression":
        raise ImportPatchException()

    def __le__(self, other: "Expression") -> "Expression":
        raise ImportPatchException()

    def __gt__(self, other: "Expression") -> "Expression":
        raise ImportPatchException()

    def __ge__(self, other: "Expression") -> "Expression":
        raise ImportPatchException()

    def __matmul__(self, other):
        return NotImplemented


class Variable(Expression):
    def __hash__(self):
        return hash((type(self), self.name))

    def __init__(self, name: str) -> None:
        Expression.__init__(self)
        self.name = name

    def __str__(self) -> str:
        return self.name

    def eval_var(self, table: VarTable) -> "Expression":
        return table.get(self.name, self)

    def diff(self, other: "Expression", start: int = 0) -> list[int] | None:
        if start > 0:
            return None
        if self == other:
            return None
        return []

    def vmatch(self, expr: Expression, matched: VarTable) -> VarTable | None:
        if matched.get(self.name, expr) != expr:
            return None
        if self.type() != expr.type():
            return None
        matched[self.name] = expr
        return matched

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        if self.type() != other.type():
            return False
        if self.name != other.name:
            return False
        return True
