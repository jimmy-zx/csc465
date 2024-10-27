"""
11.3.0, FMSD
"""

from fmsd.ast.node import Variable
from fmsd_impl.constants.basic import TRUE, FALSE
from fmsd_impl.operators.binary import And, Flip, Implies
from fmsd_impl.operators.generic import Equals, NotEquals, Ternary

x = Variable("x")
y = Variable("y")
z = Variable("z")
a = Variable("a")

axiom_reflexivity = Equals(Equals(x, x), TRUE)

axiom_symmetry = Equals(Equals(x, y), Equals(y, x))

axiom_transitivity = Implies(
    And(Equals(x, y), Equals(y, z)),
    Equals(x, z),
)

axiom_unequality = Equals(NotEquals(x, y), Flip(Equals(x, y)))

axiom_case_base_true = Equals(Ternary(TRUE, x, y), x)

axiom_case_base_false = Equals(Ternary(FALSE, x, y), y)

axiom_case_idempotent = Equals(Ternary(a, x, x), x)

axiom_case_reversal = Equals(Ternary(a, x, y), Ternary(Flip(a), y, x))
