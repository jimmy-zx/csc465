from fmsd.ast.node import Variable
from fmsd_impl.operators import And, Context, Equals, Implies

a = Variable("a")
b = Variable("b")

axiom_context_and = Equals(And(a, b), And(Context(a, b), b))
axiom_context = Implies(Context(a, b), a)
