from fmsd.expression import Expression
from fmsd.expression.constants import TRUE, FALSE
from fmsd.expression.operators.binary import Equals, And, NotEquals, Flip, Ternary
from fmsd.rule import MatchRule
from fmsd.expression.variables import BinaryVariable


x = BinaryVariable("x")
y = BinaryVariable("y")
z = BinaryVariable("z")
a = BinaryVariable("a")

rule_reflexivity = MatchRule(Equals(x, x), TRUE, equiv=True)

rule_symmetry = MatchRule(Equals(x, y), Equals(y, x))  # equiv=True is not needed

rule_transitivity = MatchRule(And(Equals(x, y), Equals(y, z)), Equals(x, z))

rule_unequality = MatchRule(NotEquals(x, y), Flip(Equals(x, y)), equiv=True)

rule_case_base_true = MatchRule(Ternary(TRUE, x, y), x, equiv=True)

rule_case_base_false = MatchRule(Ternary(FALSE, x, y), y, equiv=True)

rule_case_idempotent = MatchRule(Ternary(a, x, x), x, equiv=True)

rule_case_reversal = MatchRule(Ternary(a, x, y), Ternary(Flip(a), y, x), equiv=True)
