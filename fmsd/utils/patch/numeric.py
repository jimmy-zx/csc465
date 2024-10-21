# type: ignore
from fmsd.expression import Expression
from fmsd.expression.operators.numeric import (
    Negate,
    Plus,
    Minus,
    Multiply,
    DividedBy,
    Power,
    LessThan,
    LessThanOrEqualsTo,
    GreaterThan,
    GreaterThanOrEqualsTo,
)

# pylint: disable=unnecessary-lambda

Expression.__neg__ = lambda r: Negate(r)
Expression.__add__ = lambda l, r: Plus(l, r)
Expression.__sub__ = lambda l, r: Minus(l, r)
Expression.__mul__ = lambda l, r: Multiply(l, r)
Expression.__truediv__ = lambda l, r: DividedBy(l, r)
Expression.__pow__ = lambda l, r: Power(l, r)
Expression.__lt__ = lambda l, r: LessThan(l, r)
Expression.__le__ = lambda l, r: LessThanOrEqualsTo(l, r)
Expression.__gt__ = lambda l, r: GreaterThan(l, r)
Expression.__ge__ = lambda l, r: GreaterThanOrEqualsTo(l, r)
