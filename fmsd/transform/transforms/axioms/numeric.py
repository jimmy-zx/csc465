"""
11.3.2, FMSD
"""

import fmsd.utils.patch.binary
import fmsd.utils.patch.numeric
from fmsd.expression import Expression
from fmsd.expression.constants.binary import TRUE
from fmsd.expression.constants.numeric import ZERO, ONE, INFINITY, NEG_INFINITY
from fmsd.expression.operators.binary import Implies
from fmsd.expression.operators.generic import Equals
from fmsd.expression.variables import NumericVariable
from fmsd.utils.patchops.infix import EQ, NEQ, MAX, MIN

assert fmsd.utils.patch.numeric
assert fmsd.utils.patch.binary

x = NumericVariable("x")
y = NumericVariable("y")
z = NumericVariable("z")

axiom_identity_add = Equals(x + ZERO, x)
axiom_symmetry_add = Equals(x + y, y + x)
axiom_associative_add = Equals(x + (y + z), (x + y) + z)
axiom_cancellation_add = Implies(
    (NEG_INFINITY < x) & (x < INFINITY), ((x + y) @ EQ @ (y + z)) @ EQ @ (y @ EQ @ z)
)
axiom_absorption_add_pos = Implies(NEG_INFINITY < x, (INFINITY + x) @ EQ @ INFINITY)
axiom_absorption_add_neg = Implies(x < INFINITY, (NEG_INFINITY + x) @ EQ @ NEG_INFINITY)
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
    (NEG_INFINITY < x) & (x < INFINITY), (((x - y) @ EQ @ (y - z)) @ EQ @ (y @ EQ @ z))
)
axiom_inverse = Implies((NEG_INFINITY < x) & (x < INFINITY), (x - x) @ EQ @ ZERO)
axiom_absorption_sub_pos = Implies(x < INFINITY, (INFINITY - x) @ EQ @ INFINITY)
axiom_absorption_sub_neg = Implies(
    NEG_INFINITY < x, (NEG_INFINITY - x) @ EQ @ NEG_INFINITY
)

axiom_base_mul = Implies((NEG_INFINITY < x) & (x < INFINITY), (x * ZERO) @ EQ @ ZERO)
axiom_identity_mul = Equals((x * ONE) @ EQ @ x, TRUE)
axiom_symmetry = Equals(x * y, y * x)
axiom_distributivity_mul = Equals(x * (y + z), x * y + x * z)
axiom_associativity_mul = Equals(x * (y * z), (x * y) * z)
axiom_cancellation_mul = Implies(
    ((NEG_INFINITY < x) & (x < INFINITY)) & x @ NEQ @ ZERO,
    ((x * y) @ EQ @ (y * z)) @ EQ @ (y @ EQ @ z),
)
axiom_absorption_mul_pos = Implies(ZERO < x, (x * INFINITY) @ EQ @ INFINITY)
axiom_absorption_mul_neg = Implies(ZERO < x, (x * NEG_INFINITY) @ EQ @ NEG_INFINITY)

axiom_identity_div = Equals(x / ONE, x)
axiom_base_div_zero = Implies(x @ NEQ @ ZERO, (ZERO / x) @ EQ @ ZERO)
axiom_base_div_one = Implies(
    ((NEG_INFINITY < x) & (x < INFINITY) & (x @ NEQ @ ZERO)),
    (x / x) @ EQ @ ONE,
)

axiom_mul_div_1 = Equals(x * (y / z), (x * y) / z)
axiom_mul_div_2 = Equals((x * y) / z, (x / z) * y)
axiom_mul_div_3 = Equals((x / z) * y, x / (z / y))
axiom_mul_div_4 = Equals((x / y) / z, x / (y * z))
axiom_mul_div_id = Implies(
    ((NEG_INFINITY < y) & (y < INFINITY)) & (y @ NEQ @ ZERO),
    ((x / y) * y) @ EQ @ x,
)
axiom_annihilation_pos = Implies(
    (NEG_INFINITY < x) & (x < INFINITY), (x / INFINITY) @ EQ @ ZERO
)
axiom_annihilation_neg = Implies(
    (NEG_INFINITY < x) & (x < INFINITY), (x / NEG_INFINITY) @ EQ @ ZERO
)

axiom_base_pow = Implies((NEG_INFINITY < x) & (x < INFINITY), (x**ZERO) @ EQ @ ONE)
axiom_identity_pow = Equals(x**ONE, x)
axiom_adding_pow = Equals(x ** (y + z), (x**y) * (x**z))

# temp fix for pycharm typing issue
assert isinstance(ZERO, Expression)
assert isinstance(ONE, Expression)
axiom_direction_neg = Equals(NEG_INFINITY < ZERO, TRUE)
axiom_direction_zero = Equals(ZERO < ONE, TRUE)
axiom_direction_pos = Equals(ONE < INFINITY, TRUE)

axiom_reflection = Equals(x < y, -y < -x)
axiom_translation = Implies(
    (NEG_INFINITY < x) & (x < INFINITY), ((x + y) < (x + z)) @ EQ @ (y < z)
)
axiom_scale = Implies((ZERO < x) & (x < INFINITY), ((x * y) < (x * z)) @ EQ @ (y < z))
axiom_extremes = Equals((NEG_INFINITY <= x) & (x <= INFINITY), TRUE)

axiom_base_max = Equals(x @ MAX @ INFINITY, INFINITY)
axiom_base_min = Equals(x @ MIN @ NEG_INFINITY, NEG_INFINITY)
axiom_identity_max = Equals(x @ MAX @ NEG_INFINITY, x)
axiom_identity_min = Equals(x @ MIN @ INFINITY, x)
axiom_duality_max = Equals(-(x @ MAX @ y), (-x) @ MIN @ (-y))
axiom_duality_min = Equals(-(x @ MIN @ y), (-x) @ MAX @ (-y))
axiom_distributivity_max_pos = Equals(
    x >= ZERO, (x * (y @ MAX @ z)) @ EQ @ ((x * y) @ MAX @ (x * z))
)
axiom_distributivity_max_neg = Equals(
    x <= ZERO, (x * (y @ MAX @ z)) @ EQ @ ((x * y) @ MIN @ (x * z))
)
axiom_distributivity_min_pos = Equals(
    x >= ZERO, (x * (y @ MIN @ z)) @ EQ @ ((x * y) @ MIN @ (x * z))
)
axiom_distributivity_min_neg = Equals(
    x <= ZERO, (x * (y @ MIN @ z)) @ EQ @ ((x * y) @ MAX @ (x * z))
)

axiom_exp = Equals(x ** (y * z), (x**y) ** z)
