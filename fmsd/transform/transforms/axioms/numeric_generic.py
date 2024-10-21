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

axiom_reflexivity = Equals(x @ EQ @ x, TRUE)

axiom_symmetry = Equals(x @ EQ @ y, y @ EQ @ x)

axiom_transitivity = Implies((x @ EQ @ y) & (y @ EQ @ z), x @ EQ @ z)

axiom_unequality = Equals((x @ NEQ @ y), ~(x @ EQ @ y))

axiom_case_base_true = Equals(Ternary(TRUE, x, y), x)

axiom_case_base_false = Equals(Ternary(FALSE, x, y), y)

axiom_case_idempotent = Equals(Ternary(a, x, x), x)

axiom_case_reversal = Equals(Ternary(a, x, y), Ternary(~a, y, x))

axiom_reflexivity_le = Equals(x <= x, TRUE)

axiom_irreflexitivity_lt = Equals(x < x, FALSE)

axiom_exclusitivity_lt_eq = Equals((x < y) & (x @ EQ @ y), FALSE)

axiom_exclusitivity_gt_eq = Equals((x > y) & (x @ EQ @ y), FALSE)

axiom_exclusitivity_lt_ge = Equals((x < y) & (x > y), FALSE)

axiom_inclusitivity = Equals(x <= y, (x < y) | (x @ EQ @ y))

axiom_transitivity_le = Implies((x <= y) & (y <= z), x <= z)

axiom_transitivity_lt = Implies((x < y) & (y < z), x < z)

axiom_transitivity_lt_le = Implies((x < y) & (y <= z), x < z)

axiom_transitivity_le_lt = Implies((x <= y) & (y < z), x < z)

axiom_mirror_ge = Equals(x > y, y < x)

axiom_mirror_gt = Equals(x >= y, y <= x)

axiom_totality_lt = Equals(~(x < y), x >= y)

axiom_totality_le = Equals(~(x <= y), x > y)

axiom_trichotomy = Equals((x < y) | ((x @ EQ @ y) | (x > y)), TRUE)

axiom_antisymmetry = Equals((x <= y) & (y <= x), x @ EQ @ y)

axiom_idempotence_max = Equals(x @ MAX @ x, x)

axiom_idempotence_min = Equals(x @ MIN @ x, x)

axiom_symmetry_max = Equals(x @ MAX @ y, y @ MAX @ x)

axiom_symmetry_min = Equals(x @ MIN @ y, y @ MIN @ x)

axiom_associative_max = Equals(x @ MAX @ (y @ MAX @ z), (x @ MAX @ y) @ MAX @ z)

axiom_associative_min = Equals(x @ MIN @ (y @ MIN @ z), (x @ MIN @ y) @ MIN @ z)

axiom_distributive_max = Equals(
    x @ MAX @ (y @ MIN @ z), (x @ MAX @ y) @ MIN @ (x @ MAX @ z)
)

axiom_distributive_min = Equals(
    x @ MIN @ (y @ MAX @ z), (x @ MIN @ y) @ MAX @ (x @ MIN @ z)
)

axiom_connection_max_and = Equals((x @ MAX @ y) <= z, (x <= z) & (y <= z))

axiom_connection_max_or = Equals(x <= (y @ MAX @ z), (x <= y) | (x <= z))

axiom_connection_min_or = Equals((x @ MIN @ y) <= z, (x <= z) | (y <= z))

axiom_connection_min_and = Equals(x <= (y @ MIN @ z), (x <= y) & (y <= z))

axiom_formation_max = Equals(x @ MAX @ y, Ternary(x >= y, x, y))

axiom_formation_min = Equals(x @ MIN @ y, Ternary(x <= y, x, y))

axiom_max = Equals(x <= (x @ MAX @ y), TRUE)
