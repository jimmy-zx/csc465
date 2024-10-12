# type: ignore
from fmsd.expression.operators.numeric import Negate, Plus, Minus, Multiply, DividedBy, Power, LessThan, \
    LessThanOrEqualsTo, GreaterThan, GreaterThanOrEqualsTo
from fmsd.expression.types import NumericExpression

NumericExpression.__neg__ = lambda r: Negate(r)
NumericExpression.__add__ = lambda l, r: Plus(l, r)
NumericExpression.__sub__ = lambda l, r: Minus(l, r)
NumericExpression.__mul__ = lambda l, r: Multiply(l, r)
NumericExpression.__truediv__ = lambda l, r: DividedBy(l, r)
NumericExpression.__pow__ = lambda l, r: Power(l, r)
NumericExpression.__lt__ = lambda l, r: LessThan(l, r)
NumericExpression.__le__ = lambda l, r: LessThanOrEqualsTo(l, r)
NumericExpression.__gt__ = lambda l, r: GreaterThan(l, r)
NumericExpression.__ge__ = lambda l, r: GreaterThanOrEqualsTo(l, r)
