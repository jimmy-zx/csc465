# type: ignore
from fmsd.expression import Expression
from fmsd.expression.operators.binary import Flip, And, Or, Implies, ImpliedBy

# pylint: disable=unnecessary-lambda

Expression.__invert__ = lambda l: Flip(l)
Expression.__and__ = lambda l, r: And(l, r)
Expression.__or__ = lambda l, r: Or(l, r)
Expression.__rshift__ = lambda l, r: Implies(l, r)
Expression.__lshift__ = lambda l, r: ImpliedBy(l, r)
