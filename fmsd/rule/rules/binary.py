"""
11.3.1, FMSD
"""
from fmsd.expression.constants import TRUE, FALSE
from fmsd.expression.operators.binary import Equals, And, NotEquals, Flip, Or, Implies, ImpliedBy
from fmsd.expression.variables import BinaryVariable
from fmsd.rule import MatchRule

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")

# Page 234

rule_excluded_middle = MatchRule(Or(a, Flip(a)), TRUE)

rule_noncontradiction = MatchRule(And(a, Flip(a)), FALSE)

rule_base_and = MatchRule(And(a, FALSE), FALSE)

rule_base_or = MatchRule(Or(a, TRUE), TRUE)

rule_base_implies_true = MatchRule(Implies(a, TRUE), TRUE)

rule_base_implies_false = MatchRule(Implies(FALSE, a), TRUE)

rule_mirror = MatchRule(Implies(a, b), ImpliedBy(b, a))

rule_double_negation = MatchRule(Flip(Flip(a)), a)

rule_duality_and = MatchRule(Flip(And(a, b)), Or(Flip(a), Flip(b)))

rule_duality_or = MatchRule(Flip(Or(a, b)), And(Flip(a), Flip(b)))

rule_contrapositive = MatchRule(Implies(a, b), Implies(Flip(b), Flip(a)))

rule_exclusion = MatchRule(Equals(a, Flip(b)), NotEquals(a, b))

rule_material_implication = MatchRule(Implies(a, b), Or(Flip(a), b))

rule_inclusion_and = MatchRule(Implies(a, b), Equals(And(a, b), a))

rule_inclusion_or = MatchRule(Implies(a, b), Equals(Or(a, b), b))

# Page 235

rule_identity_and = MatchRule(And(TRUE, a), a)

rule_identity_or = MatchRule(Or(FALSE, a), a)

rule_identity_implies = MatchRule(Implies(TRUE, a), a)

rule_identity_equals = MatchRule(Equals(TRUE, a), a)

rule_idempotent_and = MatchRule(And(a, a), a)

rule_idempotent_or = MatchRule(Or(a, a), a)

rule_reflexive_implies = MatchRule(Implies(a, a), TRUE)

rule_reflexive_equals = MatchRule(Equals(a, a), TRUE)

rule_indirect_proof = MatchRule(Implies(Flip(a), FALSE), a)

rule_indirect_proof_contradiction = MatchRule(Implies(Flip(a), a), a)

rule_specialization = MatchRule(And(a, b), a, equiv=False)

rule_associative_and = MatchRule(And(a, And(b, c)), And(And(a, b), c))

rule_associative_or = MatchRule(Or(a, Or(b, c)), Or(Or(a, b), c))

rule_associative_equals = MatchRule(Equals(a, Equals(b, c)), Equals(Equals(a, b), c))

rule_associative_not_equals = MatchRule(NotEquals(a, NotEquals(b, c)), NotEquals(NotEquals(a, b), c))

rule_associative_mixed_equals = MatchRule(Equals(a, NotEquals(b, c)), NotEquals(Equals(a, b), c))
