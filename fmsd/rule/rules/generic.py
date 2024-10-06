from fmsd.expression.constants import TRUE, FALSE
from fmsd.expression.operators.binary import Equals, And, NotEquals, Flip, Ternary
from fmsd.rule import MatchRule
from fmsd.expression.variables import BinaryVariable


x = BinaryVariable("x")
y = BinaryVariable("y")
z = BinaryVariable("z")
a = BinaryVariable("a")

rule_reflexivity = MatchRule(Equals(x, x), TRUE)

rule_symmetry = MatchRule(Equals(x, y), Equals(y, x))

rule_transitivity = MatchRule(And(Equals(x, y), Equals(y, z)), Equals(x, z), equiv=False)

rule_unequality = MatchRule(NotEquals(x, y), Flip(Equals(x, y)))

rule_case_base_true = MatchRule(Ternary(TRUE, x, y), x)

rule_case_base_false = MatchRule(Ternary(FALSE, x, y), y)

rule_case_idempotent = MatchRule(Ternary(a, x, x), x)

rule_case_reversal = MatchRule(Ternary(a, x, y), Ternary(Flip(a), y, x))
