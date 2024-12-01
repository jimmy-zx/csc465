from fmsd.ast import Node
from fmsd.impl.operators import And, Equals


class Associative(Node):
    """
    Node(a, Node(b, c)) === Node(Node(a, b), c)
    """

    @staticmethod
    def has_prop(t: type) -> bool:
        if t is And:
            return True
        return issubclass(t, Associative)


class Commutative(Node):
    """
    Node(a, b) === Node(b, a)
    """

    @staticmethod
    def has_prop(t: type) -> bool:
        if t is And or t is Equals:
            return True
        return issubclass(t, Commutative)


class Idempotent(Node):
    """
    a = Node(a, a)
    """

    @staticmethod
    def has_prop(t: type) -> bool:
        if t is And:
            return True
        return issubclass(t, Idempotent)


__all__ = [
    "Associative",
    "Commutative",
    "Idempotent",
]
