from fmsd.ast.node import VarNode
from fmsd_impl.constants import TRUE
from fmsd_impl.operators import And, Context, Equals, Implies

a = VarNode("a")
b = VarNode("b")

axiom_context_and = Equals(And(a, b), And(Context(a, b), b))
axiom_context_removal = Implies(Context(a, b), a)
axiom_context_intro = Equals(a, Context(a, TRUE))
