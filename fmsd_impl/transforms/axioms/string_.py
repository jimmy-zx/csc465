import fmsd_impl.patch
from fmsd.ast import VarNode
from fmsd_impl.constants import INFINITY, NAT, NIL, NULL, ONE, ZERO
from fmsd_impl.operators import (
    And,
    Count,
    Duplicate,
    Equals,
    Implies,
    Join,
    Length,
    List,
    Replace,
    Set,
    Size,
    Star,
    StringRange,
    Subscript,
    Ternary,
    Union,
)

assert fmsd_impl.patch

A = VarNode("A")
B = VarNode("B")
C = VarNode("C")
S = VarNode("S")
T = VarNode("T")
U = VarNode("U")
i = VarNode("i")
j = VarNode("j")
n = VarNode("n")
m = VarNode("m")
x = VarNode("x")
y = VarNode("y")
z = VarNode("z")

axiom_nil_right = Equals(Join(S, NIL), S)
axiom_nil_left = Equals(Join(NIL, S), S)

axiom_length_nil = Equals(Length(NIL), ZERO)
axiom_length_join = Equals(Length(Join(S, T)), Length(S) + Length(T))

axiom_subscript_null = Equals(Subscript(S, NULL), NULL)
axiom_subscript_bunch = Equals(
    Subscript(S, Union(A, B)), Union(Subscript(S, A), Subscript(S, B))
)
axiom_subscript_set = Equals(Subscript(S, Set(A)), Set(Subscript(S, A)))
axiom_subscript_nil = Equals(Subscript(S, NIL), NIL)
axiom_subscript_string = Equals(
    Subscript(S, Join(T, U)), Join(Subscript(S, T), Subscript(S, U))
)
axiom_subscript_list = Equals(Subscript(S, List(T)), List(Subscript(S, T)))

axiom_order_nil = NIL <= S
axiom_order_length = Implies(
    And(Length(S) < INFINITY, Length(T) >= ONE), S < Join(S, T)
)
axiom_order = Implies(
    And(
        (Length(S) < INFINITY) & (i < j),
        (Equals(Length(i), ONE) & Equals(Length(j), ONE)),
    ),
    Join(Join(S, i), T) < Join(Join(S, j), U),
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
    Equals(Replace(Join(Join(S, i), T), Length(S), j), Join(Join(S, j), T)),
)
axiom_replace_subscript = Equals(
    Subscript(Replace(S, n, i), m), Ternary(Equals(n, m), i, Subscript(S, m))
)

axiom_multiply_base = Equals(Duplicate(ZERO, S), NIL)
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

axiom_distributive_bunch_left_null = Equals(Join(A, NULL), NULL)
axiom_distributive_bunch_right_null = Equals(Join(NULL, B), NULL)
axiom_distributive_bunch_left = Equals(
    Join(Union(A, B), C), Union(Join(A, C), Join(B, C))
)
axiom_distributive_bunch_right = Equals(
    Join(C, Union(A, B)), Union(Join(C, A), Join(C, B))
)
axiom_size_nil = Equals(Size(NIL), ONE)
axiom_size_distributive = Size(Join(A, B)) <= Size(A) * Size(B)

axiom_distributive_dup_null = Equals(Duplicate(NULL, A), NULL)
axiom_distributive_dup = Equals(
    Duplicate(Union(A, B), C), Union(Duplicate(A, C), Duplicate(B, C))
)
axiom_distributive_star = Equals(Star(A), Duplicate(NAT, A))
