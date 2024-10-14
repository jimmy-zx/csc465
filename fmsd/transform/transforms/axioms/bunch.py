# noinspection PyUnresolvedReferences
import fmsd.utils.patch.binary
# noinspection PyUnresolvedReferences
import fmsd.utils.patch.numeric
from fmsd.expression import Expression
from fmsd.expression.constants.bunch import NULL, NAT, XINT, XREAL
from fmsd.expression.constants.numeric import ZERO, ONE, INFINITY, NEG_INFINITY
from fmsd.expression.operators.binary import Flip
from fmsd.expression.operators.binary import Implies
from fmsd.expression.operators.bunch import In, Union, Intersect, Includes, Count, BunchInterval
from fmsd.expression.operators.generic import Equals
from fmsd.expression.variables import NumericVariable, NumericSingularVariable

x = NumericSingularVariable("x")
y = NumericSingularVariable("y")
z = NumericSingularVariable("z")
A = NumericVariable("A")
B = NumericVariable("B")
C = NumericVariable("C")
D = NumericVariable("D")

axiom_elementary = Equals(In(x, y), Equals(x, y))
axiom_compound = Equals(In(x, Union(A, B)), In(x, A) | In(x, B))
axiom_idempotence_union = Equals(Union(A, A), A)
axiom_idempotence_intersect = Equals(Intersect(A, A), A)
axiom_antidistributivity_union = Equals(In(Union(A, B), C), In(A, C) & In(B, C))
axiom_distributivity_intersect = Equals(In(A, Intersect(B, C)), In(A, B) & In(A, C))
axiom_generalization = In(A, Union(A, B))
axiom_specialization = In(Intersect(A, B), A)
axiom_reflexivity = In(A, A)
axiom_antisymmetry = Equals(In(A, B) & In(B, A), Equals(A, B))
axiom_transitivity = Implies(In(A, B) & In(B, C), In(A, C))
axiom_mirror = Equals(Includes(A, B), In(B, A))
axiom_size_null = Equals(Count(NULL), ZERO)
axiom_size_one = Equals(Count(x), ONE)
axiom_size_nat = Equals(Count(NAT), INFINITY)
axiom_size_bin = Equals(Count(Intersect(A, B)) + Count(Union(A, B)), Count(A) + Count(B))
axiom_size_notin = Equals(Flip(In(x, A)), Equals(Count(Intersect(x, A)), ZERO))
axiom_size_subset = Implies(In(A, B), Count(A) <= Count(B))
axiom_absorption_union = Equals(Union(A, Intersect(A, B)), A)
axiom_absorption_intersect = Equals(Intersect(A, Union(A, B)), A)
axiom_inclusion_union = Equals(In(A, B), Equals(Union(A, B), B))
axiom_inclusion_intersect = Equals(In(A, B), Equals(A, Intersect(A, B)))


def helper_distributive(outer, inner) -> Expression:
    return Equals(outer(A, inner(B, C)), inner(outer(A, B), outer(A, C)))


axiom_distributive_intersect_union = helper_distributive(Intersect, Union)
axiom_distributive_intersect_intersect = helper_distributive(Intersect, Intersect)
axiom_distributive_union_intersect = helper_distributive(Union, Intersect)
axiom_distributive_union_union = helper_distributive(Union, Union)

axiom_monotonicity_union = Implies(In(A, B) & In(C, D), In(Union(A, C), Union(B, D)))
axiom_monotonicity_intersect = Implies(In(A, B) & In(C, D), In(Intersect(A, C), Intersect(B, D)))
axiom_induction = In(NULL, A)
axiom_identity_left = Equals(Union(A, NULL), A)
axiom_identity_right = Equals(Union(NULL, A), A)
axiom_base_left = Equals(Intersect(A, NULL), NULL)
axiom_base_right = Equals(Intersect(NULL, A), A)
axiom_size_empty = Equals(Equals(Count(A), ZERO), Equals(A, NULL))

axiom_interval_content = Equals(In(x, BunchInterval(y, z)), In(x, XINT) & (y <= x) & (x < z))
axiom_interval_size = Equals(Count(BunchInterval(x, y)), y - x)
axiom_nat = Equals(NAT, BunchInterval(ZERO, INFINITY))
axiom_infty = In(INFINITY, x / ZERO)
axiom_neg_infty = In(NEG_INFINITY, x / ZERO)
axiom_xreal = In(XREAL, ZERO / ZERO)

axiom_distribution_null = Equals(-NULL, NULL)
axiom_distribution_neg = Equals(-Union(A, B), Union(-A, -B))
axiom_distribution_null = Equals(A + NULL, A)
axiom_distribution_add = Equals(Union(A, B) + Union(C, D), Union(Union(A + C, A + D), Union(B + C, B + D)))

# TODO