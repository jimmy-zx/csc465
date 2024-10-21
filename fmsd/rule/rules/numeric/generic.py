"""
11.3.0, FMSD
"""

import fmsd.utils.patch.binary
import fmsd.utils.patch.numeric
from fmsd.expression.constants.binary import TRUE, FALSE
from fmsd.expression.operators.binary import Implies
from fmsd.expression.operators.generic import Ternary, Equals
from fmsd.expression.variables import BinaryVariable
from fmsd.expression.variables import NumericVariable
from fmsd.utils.patchops.infix import EQ, NEQ, MAX, MIN

assert fmsd.utils.patch.binary
assert fmsd.utils.patch.numeric

x = NumericVariable("x")
y = NumericVariable("y")
z = NumericVariable("z")
a = BinaryVariable("a")

rule_reflexivity = Equals(x @ EQ @ x, TRUE)

rule_symmetry = Equals(x @ EQ @ y, y @ EQ @ x)

rule_transitivity = Implies((x @ EQ @ y) & (y @ EQ @ z), x @ EQ @ z)

rule_unequality = Equals((x @ NEQ @ y), ~(x @ EQ @ y))

rule_case_base_true = Equals(Ternary(TRUE, x, y), x)

rule_case_base_false = Equals(Ternary(FALSE, x, y), y)

rule_case_idempotent = Equals(Ternary(a, x, x), x)

rule_case_reversal = Equals(Ternary(a, x, y), Ternary(~a, y, x))

rule_reflexivity_le = Equals(x <= x, TRUE)

rule_irreflexitivity_lt = Equals(x < x, FALSE)

rule_exclusitivity_lt_eq = Equals((x < y) & (x @ EQ @ y), FALSE)

rule_exclusitivity_gt_eq = Equals((x > y) & (x @ EQ @ y), FALSE)

rule_exclusitivity_lt_ge = Equals((x < y) & (x > y), FALSE)

rule_inclusitivity = Equals(x <= y, (x < y) | (x @ EQ @ y))

rule_transitivity_le = Implies((x <= y) & (y <= z), x <= z)

rule_transitivity_lt = Implies((x < y) & (y < z), x < z)

rule_transitivity_lt_le = Implies((x < y) & (y <= z), x < z)

rule_transitivity_le_lt = Implies((x <= y) & (y < z), x < z)

rule_mirror_ge = Equals(x > y, y < x)

rule_mirror_gt = Equals(x >= y, y <= x)

rule_totality_lt = Equals(~(x < y), x >= y)

rule_totality_le = Equals(~(x <= y), x > y)

rule_trichotomy = Equals((x < y) | ((x @ EQ @ y) | (x > y)), TRUE)

rule_antisymmetry = Equals((x <= y) & (y <= x), x @ EQ @ y)

rule_idempotence_max = Equals(x @ MAX @ x, x)

rule_idempotence_min = Equals(x @ MIN @ x, x)

rule_symmetry_max = Equals(x @ MAX @ y, y @ MAX @ x)

rule_symmetry_min = Equals(x @ MIN @ y, y @ MIN @ x)

rule_associative_max = Equals(x @ MAX @ (y @ MAX @ z), (x @ MAX @ y) @ MAX @ z)

rule_associative_min = Equals(x @ MIN @ (y @ MIN @ z), (x @ MIN @ y) @ MIN @ z)

rule_distributive_max = Equals(
    x @ MAX @ (y @ MIN @ z), (x @ MAX @ y) @ MIN @ (x @ MAX @ z)
)

rule_distributive_min = Equals(
    x @ MIN @ (y @ MAX @ z), (x @ MIN @ y) @ MAX @ (x @ MIN @ z)
)

rule_connection_max_and = Equals((x @ MAX @ y) <= z, (x <= z) & (y <= z))

rule_connection_max_or = Equals(x <= (y @ MAX @ z), (x <= y) | (x <= z))

rule_connection_min_or = Equals((x @ MIN @ y) <= z, (x <= z) | (y <= z))

rule_connection_min_and = Equals(x <= (y @ MIN @ z), (x <= y) & (y <= z))

rule_formation_max = Equals(x @ MAX @ y, Ternary(x >= y, x, y))

rule_formation_min = Equals(x @ MIN @ y, Ternary(x <= y, x, y))

rule_max = Equals(x <= (x @ MAX @ y), TRUE)
