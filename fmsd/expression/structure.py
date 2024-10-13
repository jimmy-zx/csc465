from fmsd.expression import Expression
from fmsd.expression.types import Type


class Bunch(Expression):
    def __init__(self, *items: Expression, type_: Type | None = None) -> None:
        assert all(item.singular() for item in items)
        self._type = type_ or items[0].type()
        assert all(op.type() == type_ for op in items)
        Expression.__init__(self)
        self.children = list(items)

    def singular(self) -> bool:
        return len(set(self.children)) == 1

    def __eq__(self, other) -> bool:
        """
        a != Bunch(a)
        """
        if not isinstance(other, Bunch):
            return False
        return set(self.children) == set(other.children)

    def type(self) -> Type:
        return self._type

    def __str__(self) -> str:
        return ",".join(map(str, self.children))


class String(Expression):
    def __init__(self, *items: Expression, type_: Type | None = None) -> None:
        self._type = type_ or items[0].type()
        assert all(op.type() == type_ for op in items)
        Expression.__init__(self)
        self.children = list(items)

    def singular(self) -> bool:
        return all(op.singular() for op in self.children)

    def __eq__(self, other) -> bool:
        """
        a != String(a)
        """
        if not isinstance(other, String):
            return False
        return self.children == other.children

    def type(self) -> Type:
        return self._type

    def __str__(self) -> str:
        return ";".join(map(str, self.children))
