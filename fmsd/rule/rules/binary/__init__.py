"""
11.3.1, FMSD
"""

from fmsd.expression import Expression
from fmsd.expression.constants.binary import TRUE, FALSE
from fmsd.expression.operators.binary import And, Flip, Or, Implies, ImpliedBy
from fmsd.expression.operators.generic import Equals, NotEquals, Ternary
from fmsd.expression.variables import BinaryVariable

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")
d = BinaryVariable("d")
e = BinaryVariable("e")

# Page 234

rule_excluded_middle = Equals(Or(a, Flip(a)), TRUE)

rule_noncontradiction = Equals(And(a, Flip(a)), FALSE)

rule_base_and = Equals(And(a, FALSE), FALSE)

rule_base_and_rev = Equals(And(FALSE, a), FALSE)

rule_base_or = Equals(Or(a, TRUE), TRUE)

rule_base_or_rev = Equals(Or(TRUE, a), TRUE)

rule_base_implies_true = Equals(Implies(a, TRUE), TRUE)

rule_base_implies_false = Implies(FALSE, a)

rule_mirror = Equals(Implies(a, b), ImpliedBy(b, a))

rule_double_negation = Equals(Flip(Flip(a)), a)

rule_duality_and = Equals(Flip(And(a, b)), Or(Flip(a), Flip(b)))

rule_duality_or = Equals(Flip(Or(a, b)), And(Flip(a), Flip(b)))

rule_contrapositive = Equals(Implies(a, b), Implies(Flip(b), Flip(a)))

rule_exclusion = Equals(Equals(a, Flip(b)), NotEquals(a, b))

rule_material_implication = Equals(Implies(a, b), Or(Flip(a), b))

rule_inclusion_and = Equals(Implies(a, b), Equals(And(a, b), a))

rule_inclusion_or = Equals(Implies(a, b), Equals(Or(a, b), b))

# Page 235

rule_identity_and = Equals(And(TRUE, a), a)

rule_identity_and_rev = Equals(And(a, TRUE), a)

rule_identity_or = Equals(Or(FALSE, a), a)

rule_identity_or_rev = Equals(Or(a, FALSE), a)

rule_identity_implies = Equals(Implies(TRUE, a), a)

rule_identity_equals = Equals(Equals(TRUE, a), a)

rule_idempotent_and = Equals(And(a, a), a)

rule_idempotent_or = Equals(Or(a, a), a)

rule_reflexive_implies = Equals(Implies(a, a), TRUE)

rule_reflexive_equals = Equals(Equals(a, a), TRUE)

rule_indirect_proof = Equals(Implies(Flip(a), FALSE), a)

rule_indirect_proof_contradiction = Equals(Implies(Flip(a), a), a)

rule_specialization = Implies(And(a, b), a)

rule_associative_and = Equals(And(a, And(b, c)), And(And(a, b), c))

rule_associative_or = Equals(Or(a, Or(b, c)), Or(Or(a, b), c))

rule_associative_equals = Equals(Equals(a, Equals(b, c)), Equals(Equals(a, b), c))

rule_associative_not_equals = Equals(
    NotEquals(a, NotEquals(b, c)), NotEquals(NotEquals(a, b), c)
)

rule_associative_mixed_equals = Equals(
    Equals(a, NotEquals(b, c)), NotEquals(Equals(a, b), c)
)

rule_commutative_and = Equals(And(a, b), And(b, a))

rule_commutative_or = Equals(Or(a, b), Or(b, a))

rule_commutative_not_equals = Equals(NotEquals(a, b), NotEquals(b, a))

rule_antisymmetry = Equals(And(Implies(a, b), Implies(b, a)), Equals(a, b))

rule_discharge_and = Equals(And(a, Implies(a, b)), And(a, b))

rule_discharge_implies = Equals(Implies(a, And(a, b)), Implies(a, b))

rule_antomonotonic = Equals(Implies(Implies(b, c), Implies(a, c)), Implies(a, b))

rule_monotonic_and = Equals(Implies(And(a, c), And(b, c)), Implies(a, b))

rule_monotonic_or = Equals(Implies(Or(a, c), Or(b, c)), Implies(a, b))

rule_monotonic_implies = Equals(Implies(Implies(c, a), Implies(c, b)), Implies(a, b))

rule_absorption_and = Equals(And(a, Or(a, b)), a)

rule_absorption_or = Equals(Or(a, And(a, b)), a)

rule_direct_proof = Implies(And(Implies(a, b), a), b)

rule_direct_proof_contrapositive = Implies(And(Implies(a, b), Flip(b)), Flip(a))

rule_direct_proof_exclusive = Implies(And(Or(a, b), Flip(a)), b)

rule_transitive_and = Implies(And(And(a, b), And(b, c)), And(a, c))

rule_transitive_implies = Implies(And(Implies(a, b), Implies(b, c)), Implies(a, c))

rule_transitive_equals = Implies(And(Equals(a, b), Equals(b, c)), Equals(a, c))

rule_transitive_implies_equals = Implies(
    And(Implies(a, b), Equals(b, c)), Implies(a, c)
)

rule_transitive_equals_implies = Implies(
    And(Equals(a, b), Implies(b, c)), Implies(a, c)
)


def helper_distributive(outer, inner) -> Expression:
    return Equals(outer(a, inner(b, c)), inner(outer(a, b), outer(a, c)))


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

rule_generalization = Equals(Or(a, b), a)

rule_antidistributive_and = Equals(
    Implies(And(a, b), c), Or(Implies(a, c), Implies(b, c))
)
rule_antidistributive_or = Equals(
    Implies(Or(a, b), c), And(Implies(a, c), Implies(b, c))
)

rule_portation = Equals(Implies(And(a, b), c), Implies(a, Implies(b, c)))

rule_conflation_and = Equals(
    And(Implies(a, b), Implies(c, d)), Implies(And(a, c), And(b, d))
)
rule_conflation_or = Equals(
    And(Implies(a, b), Implies(c, d)), Implies(Or(a, c), Or(b, d))
)

rule_equality = Equals(Equals(a, b), Or(And(a, b), And(Flip(a), Flip(b))))
rule_difference = Equals(NotEquals(a, b), Or(And(Flip(a), b), And(b, Flip(a))))

# Page 236

rule_resolution_from = Implies(And(a, c), And(Or(a, b), Or(Flip(b), c)))
rule_resolution_equiv = Equals(
    And(Or(a, b), Or(Flip(b), c)), Or(And(a, Flip(b)), And(b, c))
)
rule_resolution_to = Implies(Or(And(a, Flip(b)), And(b, c)), Or(a, c))

rule_case_creation_implies = Equals(Ternary(b, Implies(b, a), Implies(Flip(b), a)), a)
rule_case_creation_and = Equals(Ternary(b, And(b, a), And(Flip(b), a)), a)
rule_case_creation_equals = Equals(Ternary(b, Equals(b, a), NotEquals(b, a)), a)

rule_case_absorption_then_and = Equals(Ternary(a, b, c), Ternary(a, And(a, b), c))
rule_case_absorption_then_implies = Equals(
    Ternary(a, b, c), Ternary(a, Implies(a, b), c)
)
rule_case_absorption_then_equals = Equals(Ternary(a, b, c), Ternary(a, Equals(a, b), c))
rule_case_absorption_else_and = Equals(Ternary(a, b, c), Ternary(a, b, And(Flip(a), c)))
rule_case_absorption_else_or = Equals(Ternary(a, b, c), Ternary(a, b, Or(a, c)))
rule_case_absorption_else_not_equals = Equals(
    Ternary(a, b, c), Ternary(a, b, NotEquals(a, c))
)

rule_case_analysis_and = Equals(Ternary(a, b, c), Or(And(a, b), And(Flip(a), c)))
rule_case_analysis_implies = Equals(
    Ternary(a, b, c), And(Implies(a, b), Implies(Flip(a), c))
)

rule_one_case_then_true = Equals(Ternary(a, TRUE, b), Or(a, b))
rule_one_case_then_false = Equals(Ternary(a, FALSE, b), And(Flip(a), b))
rule_one_case_else_true = Equals(Ternary(a, b, TRUE), Implies(a, b))
rule_one_case_else_false = Equals(Ternary(a, b, FALSE), And(a, b))
rule_one_case_equals = Equals(Ternary(a, b, Flip(b)), Equals(a, b))
rule_one_case_not_equals = Equals(Ternary(a, Flip(b), b), NotEquals(a, b))

rule_case_distributive_flip = Equals(
    Flip(Ternary(a, b, c)), Ternary(a, Flip(b), Flip(c))
)


def helper_case_distributive_single(op) -> Expression:
    return Equals(op(Ternary(a, b, c), d), Ternary(a, op(b, d), op(c, d)))


rule_case_distributive_single_and = helper_case_distributive_single(And)
rule_case_distributive_single_or = helper_case_distributive_single(Or)
rule_case_distributive_single_equals = helper_case_distributive_single(Equals)
rule_case_distributive_single_not_equals = helper_case_distributive_single(NotEquals)
rule_case_distributive_single_implies = helper_case_distributive_single(Implies)
rule_case_distributive_single_implied_by = helper_case_distributive_single(ImpliedBy)


def helper_case_distributive_multiple(op) -> Expression:
    return Equals(
        Ternary(a, op(b, c), op(d, e)), op(Ternary(a, b, d), Ternary(a, c, e))
    )


rule_case_distributive_multiple_and = helper_case_distributive_multiple(And)
rule_case_distributive_multiple_or = helper_case_distributive_multiple(Or)
rule_case_distributive_multiple_equals = helper_case_distributive_multiple(Equals)
rule_case_distributive_multiple_not_equals = helper_case_distributive_multiple(
    NotEquals
)
rule_case_distributive_multiple_implies = helper_case_distributive_multiple(Implies)
rule_case_distributive_multiple_implied_by = helper_case_distributive_multiple(
    ImpliedBy
)
