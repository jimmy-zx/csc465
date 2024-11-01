import fmsd_impl.patch
from fmsd.ast import Variable
from fmsd_impl.constants import INFINITY, NAT, NIL, ONE, ZERO
from fmsd_impl.operators import (
    And,
    Count,
    Duplicate,
    Equals,
    Implies,
    Join,
    Length,
    Replace,
    Set,
    Star,
    StringRange,
    Subscript,
    Ternary,
)

assert fmsd_impl.patch

A = Variable("A")
B = Variable("B")
S = Variable("S")
T = Variable("T")
U = Variable("U")
i = Variable("i")
j = Variable("j")
n = Variable("n")
m = Variable("m")
x = Variable("x")
y = Variable("y")
z = Variable("z")

axiom_nil_right = Equals(Join(S, NIL), S)
axiom_nil_left = Equals(Join(NIL, S), S)

axiom_length_nil = Equals(Length(NIL), ZERO)
axiom_length_join = Equals(Length(Join(S, T)), Length(S) + Length(T))

axiom_subscript_nil = Equals(Subscript(S, NIL), NIL)
axiom_subscript_distributive = Equals(
    Subscript(S, Join(T, U)), Join(Subscript(S, T), Subscript(S, U))
)
axiom_subscript_set = Equals(Subscript(S, Set(A)), Set(Subscript(S, A)))

axiom_order_nil = NIL <= S
axiom_order_length = Implies(
    And(Length(S) < INFINITY, Length(T) >= ONE), S < Join(S, T)
)
axiom_order = Implies(
    And(
        Length(S) < INFINITY,
        And(i < j, And(Equals(Length(i), ONE), Equals(Length(j), ONE))),
    ),
    Join(Join(S, i), T) < Join(Join(S, j), T),
)
axiom_order_equals = Implies(
    And(Length(S) < INFINITY, And(Equals(Length(i), ONE), Equals(Length(j), ONE))),
    Equals(Equals(i, j), Equals(Join(Join(S, i), T), Join(Join(S, j), T))),
)

axiom_count_nil = Equals(Count(NIL), ONE)
axiom_count_join = Count(Join(A, B)) <= Count(A) * Count(B)

axiom_subscript_index = Implies(
    And(Length(S) < INFINITY, Equals(Length(i), ONE)),
    Equals(Subscript(Join(Join(S, i), T), Length(S)), i),
)

axiom_replace_index = Implies(
    And(Length(S) < INFINITY, And(Equals(Length(i), ONE), Equals(Length(j), ONE))),
    Equals(Replace(Join(Join(S, i), T), Length(S), j), j),
)
axiom_replace_subscript = Equals(
    Subscript(Replace(S, n, i), m), Ternary(Equals(n, m), i, Subscript(S, m))
)

axiom_multiply_base = Equals(ZERO * S, NIL)
axiom_multiply_induction = Equals(Duplicate(n + ONE, S), Join(Duplicate(n, S), S))

axiom_star = Equals(Star(S), Duplicate(NAT, S))
axiom_star_base = Equals(Star(S), Star(Star(S)))

axiom_range_nil = Implies(
    And(-INFINITY < x, x < INFINITY), Equals(StringRange(x, x), NIL)
)
axiom_range_base = Implies(
    And(-INFINITY < x, x < INFINITY), Equals(StringRange(x, x + ONE), x)
)
axiom_range_induction = Equals(
    Join(StringRange(x, y), StringRange(y, z)), StringRange(x, z)
)
axiom_range_length = Equals(Length(StringRange(x, y)), y - x)
