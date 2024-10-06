"""
11.3.1, FMSD
"""
from fmsd.expression.constants import TRUE, FALSE
from fmsd.expression.operators.binary import Equals, And, NotEquals, Flip, Or, Implies, ImpliedBy, Ternary
from fmsd.expression.variables import BinaryVariable
from fmsd.rule import MatchRule

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")
d = BinaryVariable("d")
e = BinaryVariable("e")

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

rule_commutative_and = MatchRule(And(a, b), And(b, a))

rule_commutative_or = MatchRule(Or(a, b), Or(b, a))

rule_commutative_not_equals = MatchRule(NotEquals(a, b), NotEquals(b, a))

rule_antisymmetry = MatchRule(And(Implies(a, b), Implies(b, a)), Equals(a, b))

rule_discharge_and = MatchRule(And(a, Implies(a, b)), And(a, b))

rule_discharge_implies = MatchRule(Implies(a, And(a, b)), Implies(a, b))

rule_antomonotonic = MatchRule(Implies(a, b), Implies(Implies(b, c), Implies(a, c)))

rule_monotonic_and = MatchRule(Implies(a, b), Implies(And(a, c), And(b, c)))

rule_monotonic_or = MatchRule(Implies(a, b), Implies(Or(a, c), Or(b, c)))

rule_monotonic_implies = MatchRule(Implies(a, b), Implies(Implies(c, a), Implies(c, b)))

rule_absorption_and = MatchRule(And(a, Or(a, b)), a)

rule_absorption_or = MatchRule(Or(a, And(a, b)), a)

rule_direct_proof = MatchRule(And(Implies(a, b), a), b, equiv=False)

rule_direct_proof_contrapositive = MatchRule(And(Implies(a, b), Flip(b)), Flip(a), equiv=False)

rule_direct_proof_exclusive = MatchRule(And(Or(a, b), Flip(a)), b, equiv=False)

rule_transitive_and = MatchRule(And(And(a, b), And(b, c)), And(a, c), equiv=False)

rule_transitive_implies = MatchRule(And(Implies(a, b), Implies(b, c)), Implies(a, c), equiv=False)

rule_transitive_equals = MatchRule(And(Equals(a, b), Equals(b, c)), Equals(a, c), equiv=False)

rule_transitive_implies_equals = MatchRule(And(Implies(a, b), Equals(b, c)), Implies(a, c), equiv=False)

rule_transitive_equals_implies = MatchRule(And(Equals(a, b), Implies(b, c)), Implies(a, c), equiv=False)


def helper_distributive(outer, inner) -> MatchRule:
    return MatchRule(outer(a, inner(b, c)), inner(outer(a, b), outer(a, c)))


rule_distributive_and_and = helper_distributive(And, And)
rule_distributive_and_or = helper_distributive(And, Or)
rule_distributive_or_and = helper_distributive(Or, And)
rule_distributive_or_or = helper_distributive(Or, Or)
rule_distributive_or_implies = helper_distributive(Or, Implies)
rule_distributive_or_equals = helper_distributive(Or, Equals)
rule_distributive_implies_and = helper_distributive(Implies, And)
rule_distributive_implies_or = helper_distributive(Implies, Or)
rule_distributive_implies_implies = helper_distributive(Implies, Implies)
rule_distributive_implies_equals = helper_distributive(Implies, Equals)

rule_generalization = MatchRule(a, Implies(a, b))

rule_antidistributive_and = MatchRule(Implies(And(a, b), c), Or(Implies(a, c), Implies(b, c)))
rule_antidistributive_or = MatchRule(Implies(Or(a, b), c), And(Implies(a, c), Implies(b, c)))

rule_portation = MatchRule(Implies(And(a, b), c), Implies(a, Implies(b, c)))

rule_conflation_and = MatchRule(And(Implies(a, b), Implies(c, d)), Implies(And(a, c), And(b, d)))
rule_conflation_or = MatchRule(And(Implies(a, b), Implies(c, d)), Implies(Or(a, c), Or(b, d)))

rule_equality = MatchRule(Equals(a, b), Or(And(a, b), And(Flip(a), Flip(b))))
rule_difference = MatchRule(NotEquals(a, b), Or(And(Flip(a), b), And(b, Flip(a))))

# Page 236

rule_resolution_from = MatchRule(And(a, c), And(Or(a, b), Or(Flip(b), c)), equiv=False)
rule_resolution_equiv = MatchRule(And(Or(a, b), Or(Flip(b), c)), Or(And(a, Flip(b)), And(b, c)))
rule_resolution_to = MatchRule(Or(And(a, Flip(b)), And(b, c)), Or(a, c), equiv=False)

rule_case_creation_implies = MatchRule(a, Ternary(b, Implies(b, a), Implies(Flip(b), a)))
rule_case_creation_and = MatchRule(a, Ternary(b, And(b, a), And(Flip(b), a)))
rule_case_creation_equals = MatchRule(a, Ternary(b, Equals(b, a), NotEquals(b, a)))

rule_case_absorption_then_and = MatchRule(Ternary(a, b, c), Ternary(a, And(a, b), c))
rule_case_absorption_then_implies = MatchRule(Ternary(a, b, c), Ternary(a, Implies(a, b), c))
rule_case_absorption_then_equals = MatchRule(Ternary(a, b, c), Ternary(a, Equals(a, b), c))
rule_case_absorption_else_and = MatchRule(Ternary(a, b, c), Ternary(a, b, And(Flip(a), c)))
rule_case_absorption_else_or = MatchRule(Ternary(a, b, c), Ternary(a, b, Or(a, c)))
rule_case_absorption_else_not_equals = MatchRule(Ternary(a, b, c), Ternary(a, b, NotEquals(a, c)))

rule_case_analysis_and = MatchRule(Ternary(a, b, c), Or(And(a, b), And(Flip(a), c)))
rule_case_analysis_implies = MatchRule(Ternary(a, b, c), And(Implies(a, b), Implies(Flip(a), c)))

rule_one_case_then_true = MatchRule(Ternary(a, TRUE, b), Or(a, b))
rule_one_case_then_false = MatchRule(Ternary(a, FALSE, b), And(Flip(a), b))
rule_one_case_else_true = MatchRule(Ternary(a, b, TRUE), Implies(a, b))
rule_one_case_else_false = MatchRule(Ternary(a, b, FALSE), And(a, b))
rule_one_case_equals = MatchRule(Ternary(a, b, Flip(b)), Equals(a, b))
rule_one_case_not_equals = MatchRule(Ternary(a, Flip(b), b), NotEquals(a, b))

rule_case_distributive_flip = MatchRule(Flip(Ternary(a, b, c)), Ternary(a, Flip(b), Flip(c)))


def helper_case_distributive_single(op) -> MatchRule:
    return MatchRule(op(Ternary(a, b, c), d), Ternary(a, op(b, d), op(c, d)))


rule_case_distributive_single_and = helper_case_distributive_single(And)
rule_case_distributive_single_or = helper_case_distributive_single(Or)
rule_case_distributive_single_equals = helper_case_distributive_single(Equals)
rule_case_distributive_single_not_equals = helper_case_distributive_single(NotEquals)
rule_case_distributive_single_implies = helper_case_distributive_single(Implies)
rule_case_distributive_single_implied_by = helper_case_distributive_single(ImpliedBy)


def helper_case_distributive_multiple(op) -> MatchRule:
    return MatchRule(Ternary(a, op(b, c), op(d, e)), op(Ternary(a, b, d), Ternary(a, c, e)))


rule_case_distributive_multiple_and = helper_case_distributive_multiple(And)
rule_case_distributive_multiple_or = helper_case_distributive_multiple(Or)
rule_case_distributive_multiple_equals = helper_case_distributive_multiple(Equals)
rule_case_distributive_multiple_not_equals = helper_case_distributive_multiple(NotEquals)
rule_case_distributive_multiple_implies = helper_case_distributive_multiple(Implies)
rule_case_distributive_multiple_implied_by = helper_case_distributive_multiple(ImpliedBy)
