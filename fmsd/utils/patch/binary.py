# type: ignore
from fmsd.ast.node import Node
from fmsd_impl.operators.binary import Flip, And, Or, Implies, ImpliedBy

# pylint: disable=unnecessary-lambda

Node.__invert__ = lambda l: Flip(l)
Node.__and__ = lambda l, r: And(l, r)
Node.__or__ = lambda l, r: Or(l, r)
Node.__rshift__ = lambda l, r: Implies(l, r)
Node.__lshift__ = lambda l, r: ImpliedBy(l, r)
