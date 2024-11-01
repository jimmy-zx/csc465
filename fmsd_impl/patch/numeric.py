# type: ignore
from fmsd.ast.node import Node
from fmsd_impl.operators.numeric import (
    DividedBy,
    GreaterThan,
    GreaterThanOrEqualsTo,
    LessThan,
    LessThanOrEqualsTo,
    Minus,
    Multiply,
    Negate,
    Plus,
    Power,
)

# pylint: disable=unnecessary-lambda

Node.__neg__ = lambda r: Negate(r)
Node.__add__ = lambda l, r: Plus(l, r)
Node.__sub__ = lambda l, r: Minus(l, r)
Node.__mul__ = lambda l, r: Multiply(l, r)
Node.__truediv__ = lambda l, r: DividedBy(l, r)
Node.__pow__ = lambda l, r: Power(l, r)
Node.__lt__ = lambda l, r: LessThan(l, r)
Node.__le__ = lambda l, r: LessThanOrEqualsTo(l, r)
Node.__gt__ = lambda l, r: GreaterThan(l, r)
Node.__ge__ = lambda l, r: GreaterThanOrEqualsTo(l, r)
