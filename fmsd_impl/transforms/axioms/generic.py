"""
11.3.0, FMSD
"""

import fmsd_impl.patch.binary
import fmsd_impl.patch.numeric
from fmsd.ast.node import Variable
from fmsd_impl.constants import FALSE, TRUE
from fmsd_impl.operators import Equals, Implies, Max, Min, Ternary
from fmsd_impl.patch.infix import EQ, NEQ

assert fmsd_impl.patch.numeric
assert fmsd_impl.patch.binary

x = Variable("x")
y = Variable("y")
z = Variable("z")
a = Variable("a")

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

axiom_idempotence_max = Equals(Max(x, x), x)

axiom_idempotence_min = Equals(Min(x, x), x)

axiom_distributive_max = Equals(Max(x, Min(y, z)), Min(Max(x, y), Max(x, z)))

axiom_distributive_min = Equals(Min(x, Max(y, z)), Max(Min(x, y), Min(x, z)))

axiom_connection_max_and = Equals(Max(x, y) <= z, (x <= z) & (y <= z))

axiom_connection_max_or = Equals(x <= Max(y, z), (x <= y) | (x <= z))

axiom_connection_min_or = Equals(Min(x, y) <= z, (x <= z) | (y <= z))

axiom_connection_min_and = Equals(x <= Min(y, z), (x <= y) & (y <= z))

axiom_formation_max = Equals(Max(x, y), Ternary(x >= y, x, y))

axiom_formation_min = Equals(Min(x, y), Ternary(x <= y, x, y))

axiom_max = Equals(x <= Max(x, y), TRUE)
