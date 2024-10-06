from fmsd.expression.constants import TRUE, FALSE
from fmsd.expression.operators.binary import Equals, And, NotEquals, Flip, Or, Implies, ImpliedBy
from fmsd.expression.variables import BinaryVariable
from fmsd.rule import MatchRule

a = BinaryVariable("a")
b = BinaryVariable("b")

rule_excluded_middle = MatchRule(Or(a, Flip(a)), TRUE, equiv=True)

rule_noncontradiction = MatchRule(And(a, Flip(a)), FALSE, equiv=True)

rule_base_and = MatchRule(And(a, FALSE), FALSE, equiv=True)

rule_base_or = MatchRule(Or(a, TRUE), TRUE, equiv=True)

rule_base_implies_true = MatchRule(Implies(a, TRUE), TRUE, equiv=True)

rule_base_implies_false = MatchRule(Implies(FALSE, a), TRUE, equiv=True)

rule_mirror = MatchRule(Implies(a, b), ImpliedBy(b, a), equiv=True)

rule_double_negation = MatchRule(Flip(Flip(a)), a, equiv=True)

rule_duality_and = MatchRule(Flip(And(a, b)), Or(Flip(a), Flip(b)), equiv=True)

rule_duality_or = MatchRule(Flip(Or(a, b)), And(Flip(a), Flip(b)), equiv=True)

rule_contrapositive = MatchRule(Implies(a, b), Implies(Flip(b), Flip(a)), equiv=True)

rule_exclusion = MatchRule(Equals(a, Flip(b)), NotEquals(a, b), equiv=True)

rule_material_implication = MatchRule(Implies(a, b), Or(Flip(a), b), equiv=True)

rule_inclusion_and = MatchRule(Implies(a, b), Equals(And(a, b), a), equiv=True)

rule_inclusion_or = MatchRule(Implies(a, b), Equals(Or(a, b), b), equiv=True)
