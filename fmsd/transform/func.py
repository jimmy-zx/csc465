from typing import Callable

from fmsd.expression import Expression
from fmsd.transform import Transform


class FunctionTransform(Transform):
    def __init__(self, func: Callable[[Expression, Expression], bool]) -> None:
        Transform.__init__(self)
        self.func = func

    def verify(self, src: Expression, dst: Expression) -> bool:
        return self.func(src, dst)
