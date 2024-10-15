# noinspection PyUnresolvedReferences
import fmsd.utils.patch.binary
# noinspection PyUnresolvedReferences
import fmsd.utils.patch.numeric
from fmsd.expression.constants.bunch import NAT
from fmsd.expression.constants.numeric import ZERO, ONE, INFINITY
from fmsd.expression.operators.binary import Implies
from fmsd.expression.operators.bunch import In, Union
from fmsd.expression.variables import NumericVariable

x = NumericVariable("x")
y = NumericVariable("y")
B = NumericVariable("B")
axiom_nat_0 = In(ZERO, NAT)
axiom_nat_1 = In(NAT + ONE, NAT)
axiom_nat_2 = Implies(In(Union(ZERO, B + ONE), B), In(NAT, B))
axiom_nat_closure_sum = Implies(In(x, NAT) & In(y, NAT), In(x + y, NAT))
axiom_nat_closure_mul = Implies(In(x, NAT) & In(y, NAT), In(x * y, NAT))
axiom_nat_min = Implies(In(x, NAT), x >= ZERO)
axiom_nat_max = Implies(In(x, NAT), x < INFINITY)
