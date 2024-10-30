import fmsd_impl.patch.binary
import fmsd_impl.patch.numeric
from fmsd.ast.node import Variable
from fmsd_impl.constants.basic import NAT, ZERO, ONE, INFINITY
from fmsd_impl.operators.binary import Implies
from fmsd_impl.operators.bunch import (
    In,
    Union,
)
from fmsd_impl.operators.generic import Equals

assert fmsd_impl.patch.binary
assert fmsd_impl.patch.numeric

x = Variable("x")
y = Variable("y")
B = Variable("B")
axiom_nat_0 = In(ZERO, NAT)
axiom_nat_1 = In(NAT + ONE, NAT)
axiom_nat_2 = Implies(In(Union(ZERO, B + ONE), B), In(NAT, B))
axiom_nat_closure_sum = Implies(In(x, NAT) & In(y, NAT), In(x + y, NAT))
axiom_nat_closure_mul = Implies(In(x, NAT) & In(y, NAT), In(x * y, NAT))
axiom_nat_min = Implies(In(x, NAT), x >= ZERO)
axiom_nat_max = Implies(In(x, NAT), x < INFINITY)

axiom_elementary_zero = Equals(In(x, ZERO), Equals(x, ZERO))
