"""
11.3.0, FMSD
"""

import fmsd.utils.patch.binary
import fmsd.utils.patch.numeric
from fmsd.expression.constants.binary import TRUE, FALSE
from fmsd.expression.operators.generic import Ternary
from fmsd.expression.variables import BinaryVariable
from fmsd.expression.variables import NumericVariable
from fmsd.rule import MatchRule
from fmsd.utils.patchops.infix import EQ, NEQ, MAX, MIN

assert fmsd.utils.patch.binary
assert fmsd.utils.patch.numeric

x = NumericVariable("x")
y = NumericVariable("y")
z = NumericVariable("z")
a = BinaryVariable("a")

rule_reflexivity = MatchRule(x @ EQ @ x, TRUE)

rule_symmetry = MatchRule(x @ EQ @ y, y @ EQ @ x)

rule_transitivity = MatchRule((x @ EQ @ y) & (y @ EQ @ z), x @ EQ @ z, equiv=False)

rule_unequality = MatchRule((x @ NEQ @ y), ~(x @ EQ @ y))

rule_case_base_true = MatchRule(Ternary(TRUE, x, y), x)

rule_case_base_false = MatchRule(Ternary(FALSE, x, y), y)

rule_case_idempotent = MatchRule(Ternary(a, x, x), x)

rule_case_reversal = MatchRule(Ternary(a, x, y), Ternary(~a, y, x))

rule_reflexivity_le = MatchRule(x <= x, TRUE)

rule_irreflexitivity_lt = MatchRule(x < x, FALSE)

rule_exclusitivity_lt_eq = MatchRule((x < y) & (x @ EQ @ y), FALSE)

rule_exclusitivity_gt_eq = MatchRule((x > y) & (x @ EQ @ y), FALSE)

rule_exclusitivity_lt_ge = MatchRule((x < y) & (x > y), FALSE)

rule_inclusitivity = MatchRule(x <= y, (x < y) | (x @ EQ @ y))

rule_transitivity_le = MatchRule((x <= y) & (y <= z), x <= z, equiv=False)

rule_transitivity_lt = MatchRule((x < y) & (y < z), x < z, equiv=False)

rule_transitivity_lt_le = MatchRule((x < y) & (y <= z), x < z, equiv=False)

rule_transitivity_le_lt = MatchRule((x <= y) & (y < z), x < z, equiv=False)

rule_mirror_ge = MatchRule(x > y, y < x)

rule_mirror_gt = MatchRule(x >= y, y <= x)

rule_totality_lt = MatchRule(~(x < y), x >= y)

rule_totality_le = MatchRule(~(x <= y), x > y)

rule_trichotomy = MatchRule((x < y) | ((x @ EQ @ y) | (x > y)), TRUE)

rule_antisymmetry = MatchRule((x <= y) & (y <= x), x @ EQ @ y)

rule_idempotence_max = MatchRule(x @ MAX @ x, x)

rule_idempotence_min = MatchRule(x @ MIN @ x, x)

rule_symmetry_max = MatchRule(x @ MAX @ y, y @ MAX @ x)

rule_symmetry_min = MatchRule(x @ MIN @ y, y @ MIN @ x)

rule_associative_max = MatchRule(x @ MAX @ (y @ MAX @ z), (x @ MAX @ y) @ MAX @ z)

rule_associative_min = MatchRule(x @ MIN @ (y @ MIN @ z), (x @ MIN @ y) @ MIN @ z)

rule_distributive_max = MatchRule(x @ MAX @ (y @ MIN @ z), (x @ MAX @ y) @ MIN @ (x @ MAX @ z))

rule_distributive_min = MatchRule(x @ MIN @ (y @ MAX @ z), (x @ MIN @ y) @ MAX @ (x @ MIN @ z))

rule_connection_max_and = MatchRule((x @ MAX @ y) <= z, (x <= z) & (y <= z))

rule_connection_max_or = MatchRule(x <= (y @ MAX @ z), (x <= y) | (x <= z))

rule_connection_min_or = MatchRule((x @ MIN @ y) <= z, (x <= z) | (y <= z))

rule_connection_min_and = MatchRule(x <= (y @ MIN @ z), (x <= y) & (y <= z))

rule_formation_max = MatchRule(x @ MAX @ y, Ternary(x >= y, x, y))

rule_formation_min = MatchRule(x @ MIN @ y, Ternary(x <= y, x, y))

rule_max = MatchRule(x <= (x @ MAX @ y), TRUE)
