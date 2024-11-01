"""
11.3.2, FMSD
"""

import fmsd_impl.patch.binary
import fmsd_impl.patch.numeric
from fmsd.ast.node import Node, Variable
from fmsd_impl.constants import TRUE, ZERO, ONE, INFINITY
from fmsd_impl.operators import Implies, Equals, Max, Min
from fmsd_impl.patch.infix import EQ, NEQ

assert fmsd_impl.patch.binary
assert fmsd_impl.patch.numeric

x = Variable("x")
y = Variable("y")
z = Variable("z")

axiom_identity_add = Equals(x + ZERO, x)
axiom_symmetry_add = Equals(x + y, y + x)
axiom_associative_add = Equals(x + (y + z), (x + y) + z)
axiom_cancellation_add = Implies(
    (-INFINITY < x) & (x < INFINITY), ((x + y) @ EQ @ (y + z)) @ EQ @ (y @ EQ @ z)
)
axiom_absorption_add_pos = Implies(-INFINITY < x, (INFINITY + x) @ EQ @ INFINITY)
axiom_absorption_add_neg = Implies(x < INFINITY, (-INFINITY + x) @ EQ @ -INFINITY)
axiom_negation = Equals(-x, ZERO - x)
axiom_self_inverse = Equals(-(-x), x)
axiom_distributivity_and = Equals(-(x + y), -x + -y)
axiom_antisymmetry = Equals(-(x - y), y - x)

axiom_semi_distributivity_mult_outer = Equals((-x) * y, -(x * y))
axiom_semi_distributivity_mult_inner = Equals((-x) * y, x * (-y))
axiom_semi_distributivity_div_outer = Equals((-x) / y, -(x / y))
axiom_semi_distributivity_div_inner = Equals((-x) / y, x / (-y))

axiom_identity_sub = Equals(x - ZERO, x)
axiom_subtraction = Equals(x - y, x + (-y))
axiom_associativity_sub = Equals(x + (y - z), (x + y) - z)
axiom_cancellation_sub = Implies(
    (-INFINITY < x) & (x < INFINITY), (((x - y) @ EQ @ (y - z)) @ EQ @ (y @ EQ @ z))
)
axiom_inverse = Implies((-INFINITY < x) & (x < INFINITY), (x - x) @ EQ @ ZERO)
axiom_absorption_sub_pos = Implies(x < INFINITY, (INFINITY - x) @ EQ @ INFINITY)
axiom_absorption_sub_neg = Implies(-INFINITY < x, (-INFINITY - x) @ EQ @ -INFINITY)

axiom_base_mul = Implies((-INFINITY < x) & (x < INFINITY), (x * ZERO) @ EQ @ ZERO)
axiom_identity_mul = Equals((x * ONE) @ EQ @ x, TRUE)
axiom_symmetry = Equals(x * y, y * x)
axiom_distributivity_mul = Equals(x * (y + z), x * y + x * z)
axiom_associativity_mul = Equals(x * (y * z), (x * y) * z)
axiom_cancellation_mul = Implies(
    ((-INFINITY < x) & (x < INFINITY)) & x @ NEQ @ ZERO,
    ((x * y) @ EQ @ (y * z)) @ EQ @ (y @ EQ @ z),
)
axiom_absorption_mul_pos = Implies(ZERO < x, (x * INFINITY) @ EQ @ INFINITY)
axiom_absorption_mul_neg = Implies(ZERO < x, (x * -INFINITY) @ EQ @ -INFINITY)

axiom_identity_div = Equals(x / ONE, x)
axiom_base_div_zero = Implies(x @ NEQ @ ZERO, (ZERO / x) @ EQ @ ZERO)
axiom_base_div_one = Implies(
    ((-INFINITY < x) & (x < INFINITY) & (x @ NEQ @ ZERO)),
    (x / x) @ EQ @ ONE,
)

axiom_mul_div_1 = Equals(x * (y / z), (x * y) / z)
axiom_mul_div_2 = Equals((x * y) / z, (x / z) * y)
axiom_mul_div_3 = Equals((x / z) * y, x / (z / y))
axiom_mul_div_4 = Equals((x / y) / z, x / (y * z))
axiom_mul_div_id = Implies(
    ((-INFINITY < y) & (y < INFINITY)) & (y @ NEQ @ ZERO),
    ((x / y) * y) @ EQ @ x,
)
axiom_annihilation_pos = Implies(
    (-INFINITY < x) & (x < INFINITY), (x / INFINITY) @ EQ @ ZERO
)
axiom_annihilation_neg = Implies(
    (-INFINITY < x) & (x < INFINITY), (x / -INFINITY) @ EQ @ ZERO
)

axiom_base_pow = Implies((-INFINITY < x) & (x < INFINITY), (x**ZERO) @ EQ @ ONE)
axiom_identity_pow = Equals(x**ONE, x)
axiom_adding_pow = Equals(x ** (y + z), (x**y) * (x**z))

# temp fix for pycharm typing issue
assert isinstance(ZERO, Node)
assert isinstance(ONE, Node)
axiom_direction_neg = Equals(-INFINITY < ZERO, TRUE)
axiom_direction_zero = Equals(ZERO < ONE, TRUE)
axiom_direction_pos = Equals(ONE < INFINITY, TRUE)

axiom_reflection = Equals(x < y, -y < -x)
axiom_translation = Implies(
    (-INFINITY < x) & (x < INFINITY), ((x + y) < (x + z)) @ EQ @ (y < z)
)
axiom_scale = Implies((ZERO < x) & (x < INFINITY), ((x * y) < (x * z)) @ EQ @ (y < z))
axiom_extremes = Equals((-INFINITY <= x) & (x <= INFINITY), TRUE)

axiom_base_max = Equals(Max(x, INFINITY), INFINITY)
axiom_base_min = Equals(Max(x, -INFINITY), -INFINITY)
axiom_identity_max = Equals(Max(x, -INFINITY), x)
axiom_identity_min = Equals(Min(x, INFINITY), x)
axiom_duality_max = Equals(-Max(x, y), Min(-x, -y))
axiom_duality_min = Equals(-Min(x, y), Max(-x, -y))
axiom_distributivity_max_pos = Equals(
    x >= ZERO, (x * Max(y, z)) @ EQ @ Max(x * y, x * z)
)
axiom_distributivity_max_neg = Equals(
    x <= ZERO, (x * Max(y, z)) @ EQ @ Min(x * y, x * z)
)
axiom_distributivity_min_pos = Equals(
    x >= ZERO, (x * Min(y, z)) @ EQ @ Min(x * y, x * z)
)
axiom_distributivity_min_neg = Equals(
    x <= ZERO, (x * Min(y, z)) @ EQ @ Max(x * y, x * z)
)

axiom_exp = Equals(x ** (y * z), (x**y) ** z)
