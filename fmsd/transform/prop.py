from fmsd.expression import Expression
from fmsd.expression.operators import AssociativeOperator, CommutativeOperator
from fmsd.transform import Transform


class AssociativeTransform(Transform):
    def __init__(self) -> None:
        Transform.__init__(self)
        self.name = "associative"

    def verify(self, src: Expression, dst: Expression) -> bool:
        if type(src) != type(dst):
            return False
        if not isinstance(src, AssociativeOperator):
            return False
        if not isinstance(src, CommutativeOperator):
            return src.collect() == dst.collect()
        else:
            return set(src.collect()) == set(dst.collect())


class CommutativeTransform(Transform):
    def __init__(self) -> None:
        Transform.__init__(self)
        self.name = "commutative"

    def verify(self, src: Expression, dst: Expression) -> bool:
        if type(src) != type(dst):
            return False
        if not isinstance(src, CommutativeOperator):
            return False
        return set(src.children) == set(dst.children)
