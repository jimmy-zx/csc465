"""
11.3.0, FMSD
"""

from fmsd.expression.constants.binary import TRUE, FALSE
from fmsd.expression.operators.binary import And, Flip, Implies
from fmsd.expression.operators.generic import Equals, NotEquals, Ternary
from fmsd.expression.variables import BinaryVariable


x = BinaryVariable("x")
y = BinaryVariable("y")
z = BinaryVariable("z")
a = BinaryVariable("a")

rule_reflexivity = Equals(Equals(x, x), TRUE)

rule_symmetry = Equals(Equals(x, y), Equals(y, x))

rule_transitivity = Implies(
    And(Equals(x, y), Equals(y, z)),
    Equals(x, z),
)

rule_unequality = Equals(NotEquals(x, y), Flip(Equals(x, y)))

rule_case_base_true = Equals(Ternary(TRUE, x, y), x)

rule_case_base_false = Equals(Ternary(FALSE, x, y), y)

rule_case_idempotent = Equals(Ternary(a, x, x), x)

rule_case_reversal = Equals(Ternary(a, x, y), Ternary(Flip(a), y, x))
