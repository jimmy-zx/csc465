"""
11.3.2, FMSD
"""
# noinspection PyUnresolvedReferences
import fmsd.utils.patch.binary
# noinspection PyUnresolvedReferences
import fmsd.utils.patch.numeric
from fmsd.expression import Expression
from fmsd.expression.constants.binary import TRUE
from fmsd.expression.constants.numeric import ZERO, ONE, INFINITY, NEG_INFINITY
from fmsd.expression.variables import NumericVariable
from fmsd.rule import MatchRule
from fmsd.utils.patchops.infix import EQ, NEQ, MAX, MIN

x = NumericVariable("x")
y = NumericVariable("y")
z = NumericVariable("z")

rule_identity_add = MatchRule(x + ZERO, x)
rule_symmetry_add = MatchRule(x + y, y + x)
rule_associative_add = MatchRule(x + (y + z), (x + y) + z)
rule_cancellation_add = MatchRule((NEG_INFINITY < x) & (x < INFINITY), ((x + y) @ EQ @ (y + z)) @ EQ @ (y @ EQ @ z),
                                  equiv=False)
rule_absorption_add_pos = MatchRule(NEG_INFINITY < x, (INFINITY + x) @ EQ @ INFINITY, equiv=False)
rule_absorption_add_neg = MatchRule(x < INFINITY, (NEG_INFINITY + x) @ EQ @ NEG_INFINITY, equiv=False)
rule_negation = MatchRule(-x, ZERO - x)
rule_self_inverse = MatchRule(--x, x)
rule_distributivity_and = MatchRule(-(x + y), -x + -y)
rule_antisymmetry = MatchRule(-(x - y), y - x)

rule_semi_distributivity_mult_outer = MatchRule((-x) * y, -(x * y))
rule_semi_distributivity_mult_inner = MatchRule((-x) * y, x * (-y))
rule_semi_distributivity_div_outer = MatchRule((-x) / y, -(x / y))
rule_semi_distributivity_div_inner = MatchRule((-x) / y, x / (-y))

rule_identity_sub = MatchRule(x - ZERO, x)
rule_subtraction = MatchRule(x - y, x + (-y))
rule_associativity_sub = MatchRule(x + (y - z), (x + y) - z)
rule_cancellation_sub = MatchRule((NEG_INFINITY < x) & (x < INFINITY), (((x - y) @ EQ @ (y - z)) @ EQ @ (y @ EQ @ z)),
                                  equiv=False)
rule_inverse = MatchRule((NEG_INFINITY < x) & (x < INFINITY), (x - x) @ EQ @ ZERO, equiv=False)
rule_absorption_sub_pos = MatchRule(x < INFINITY, (INFINITY - x) @ EQ @ INFINITY, equiv=False)
rule_absorption_sub_neg = MatchRule(NEG_INFINITY < x, (NEG_INFINITY - x) @ EQ @ NEG_INFINITY, equiv=False)

rule_base_mul = MatchRule((NEG_INFINITY < x) & (x < INFINITY), (x * ZERO) @ EQ @ ZERO, equiv=False)
rule_identity_mul = MatchRule((x * ONE) @ EQ @ x, TRUE)
rule_symmetry = MatchRule(x * y, y * x)
rule_distributivity_mul = MatchRule(x * (y + z), x * y + x * z)
rule_associativity_mul = MatchRule(x * (y * z), (x * y) * z)
rule_cancellation_mul = MatchRule(((NEG_INFINITY < x) & (x < INFINITY)) & x @ NEQ @ ZERO,
                                  ((x * y) @ EQ @ (y * z)) @ EQ @ (y @ EQ @ z), equiv=False)
rule_absorption_mul_pos = MatchRule(ZERO < x, (x * INFINITY) @ EQ @ INFINITY, equiv=False)
rule_absorption_mul_neg = MatchRule(ZERO < x, (x * NEG_INFINITY) @ EQ @ NEG_INFINITY, equiv=False)

rule_identity_div = MatchRule(x / ONE, x)
rule_base_div_zero = MatchRule(x @ NEQ @ ZERO, (ZERO / x) @ EQ @ ZERO, equiv=False)
rule_base_div_one = MatchRule(((NEG_INFINITY < x) & (x < INFINITY) & (x @ NEQ @ ZERO)), (x / x) @ EQ @ ONE, equiv=False)

rule_mul_div_1 = MatchRule(x * (y / z), (x * y) / z)
rule_mul_div_2 = MatchRule((x * y) / z, (x / z) * y)
rule_mul_div_3 = MatchRule((x / z) * y, x / (z / y))
rule_mul_div_4 = MatchRule((x / y) / z, x / (y * z))
rule_mul_div_id = MatchRule(((NEG_INFINITY < y) & (y < INFINITY)) & (y @ NEQ @ ZERO), ((x / y) * y) @ EQ @ x,
                            equiv=False)
rule_annihilation_pos = MatchRule((NEG_INFINITY < x) & (x < INFINITY), (x / INFINITY) @ EQ @ ZERO, equiv=False)
rule_annihilation_neg = MatchRule((NEG_INFINITY < x) & (x < INFINITY), (x / NEG_INFINITY) @ EQ @ ZERO, equiv=False)

rule_base_pow = MatchRule((NEG_INFINITY < x) & (x < INFINITY), (x ** ZERO) @ EQ @ ONE, equiv=False)
rule_identity_pow = MatchRule(x ** ONE, x)
rule_adding_pow = MatchRule(x ** (y + z), (x ** y) * (x ** z))

# temp fix for pycharm typing issue
assert isinstance(ZERO, Expression)
assert isinstance(ONE, Expression)
rule_direction_neg = MatchRule(NEG_INFINITY < ZERO, TRUE)
rule_direction_zero = MatchRule(ZERO < ONE, TRUE)
rule_direction_pos = MatchRule(ONE < INFINITY, TRUE)

rule_reflection = MatchRule(x < y, -y < -x)
rule_translation = MatchRule((NEG_INFINITY < x) & (x < INFINITY), ((x + y) < (x + z)) @ EQ @ (y < z), equiv=False)
rule_scale = MatchRule((ZERO < x) & (x < INFINITY), ((x * y) < (x * z)) @ EQ @ (y < z), equiv=False)
rule_extremes = MatchRule((NEG_INFINITY <= x) & (x <= INFINITY), TRUE)

rule_base_max = MatchRule(x @ MAX @ INFINITY, INFINITY)
rule_base_min = MatchRule(x @ MIN @ NEG_INFINITY, NEG_INFINITY)
rule_identity_max = MatchRule(x @ MAX @ NEG_INFINITY, x)
rule_identity_min = MatchRule(x @ MIN @ INFINITY, x)
rule_duality_max = MatchRule(-(x @ MAX @ y), (-x) @ MIN @ (-y))
rule_duality_min = MatchRule(-(x @ MIN @ y), (-x) @ MAX @ (-y))
rule_distributivity_max_pos = MatchRule(x >= ZERO, (x * (y @ MAX @ z)) @ EQ @ ((x * y) @ MAX @ (x * z)))
rule_distributivity_max_neg = MatchRule(x <= ZERO, (x * (y @ MAX @ z)) @ EQ @ ((x * y) @ MIN @ (x * z)))
rule_distributivity_min_pos = MatchRule(x >= ZERO, (x * (y @ MIN @ z)) @ EQ @ ((x * y) @ MIN @ (x * z)))
rule_distributivity_min_neg = MatchRule(x <= ZERO, (x * (y @ MIN @ z)) @ EQ @ ((x * y) @ MAX @ (x * z)))

rule_exp = MatchRule(x ** (y * z), (x ** y) ** z)
