from fmsd.expression.operators.context import Context
from fmsd.expression.operators.generic import Equals
from fmsd.expression.operators.binary import And, Implies
from fmsd.expression.variables import BinaryVariable

a = BinaryVariable("a")
b = BinaryVariable("b")

axiom_context_and = Equals(And(a, b), And(Context(a, b), b))
axiom_context = Implies(Context(a, b), a)