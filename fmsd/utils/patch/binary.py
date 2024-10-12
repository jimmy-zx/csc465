#type: ignore
from fmsd.expression.operators.binary import Flip, And, Or, Implies, ImpliedBy
from fmsd.expression.types import BinaryExpression

BinaryExpression.__invert__ = lambda l: Flip(l)
BinaryExpression.__and__ = lambda l, r: And(l, r)
BinaryExpression.__or__ = lambda l, r: Or(l, r)
BinaryExpression.__rshift__ = lambda l, r: Implies(l, r)
BinaryExpression.__lshift__ = lambda l, r: ImpliedBy(l, r)
