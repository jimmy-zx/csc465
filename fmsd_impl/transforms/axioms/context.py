from fmsd_impl.operators import Context, Equals, And, Implies
from fmsd.ast.node import Variable

a = Variable("a")
b = Variable("b")

axiom_context_and = Equals(And(a, b), And(Context(a, b), b))
axiom_context = Implies(Context(a, b), a)
