from fmsd.ast import Node


class Associative(Node):
    """
    Node(a, Node(b, c)) === Node(Node(a, b), c)
    """


class Commutative(Node):
    """
    Node(a, b) === Node(b, a)
    """


class Idempotent(Node):
    """
    a = Node(a, a)
    """


__all__ = [
    "Associative",
    "Commutative",
    "Idempotent",
]
