from fmsd.expression import Expression


class Bunch(Expression):
    def __init__(self, *items: Expression) -> None:
        assert all(item.singular() for item in items)
        Expression.__init__(self)
        self.children = list(items)

    def singular(self) -> bool:
        return len(set(self.children)) == 1
