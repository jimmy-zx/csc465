from fmsd.ast import Variable
from fmsd_impl.constants import NIL, NULL, ONE, ZERO
from fmsd_impl.operators import (
    Count,
    Equals,
    In,
    Join,
    Length,
    LessThan,
    List,
    ListAt,
    ListCompose,
    ListContents,
    ListDomain,
    ListJoin,
    ListLength,
    ListReplace,
    NotEquals,
    Replace,
    Set,
    StringRange,
    Subscript,
    Ternary,
    Union,
)

A = Variable("A")
B = Variable("B")
S = Variable("S")
T = Variable("T")
L = Variable("L")
i = Variable("i")
n = Variable("n")
m = Variable("m")
M = Variable("M")
N = Variable("N")

axiom_list_structure = NotEquals(List(S), S)
axiom_list_contents = Equals(S, ListContents(List(S)))
axiom_list_contents_rev = Equals(List(ListContents(L)), L)
axiom_list_bunch_null = Equals(List(NULL), NULL)
axiom_list_bunch = Equals(List(Union(A, B)), Union(List(A), List(B)))

axiom_list_join = Equals(ListJoin(List(S), List(T)), List(Join(S, T)))
axiom_list_equals = Equals(Equals(List(S), List(T)), Equals(S, T))
axiom_list_order = Equals(LessThan(List(S), List(T)), LessThan(S, T))

axiom_list_in = Equals(In(List(A), List(B)), In(A, B))
axiom_list_length = Equals(ListLength(List(S)), Length(S))
axiom_list_length_domain = Equals(ListLength(L), Count(ListDomain(L)))

axiom_list_replacement_nil = Equals(ListReplace(NIL, i, L), i)
axiom_list_replacement = Equals(ListReplace(n, i, List(S)), List(Replace(S, n, i)))
axiom_list_replacement_index = Equals(
    ListCompose(ListReplace(n, i, L), m), Ternary(Equals(n, m), i, ListCompose(L, m))
)

axiom_list_domain = Equals(ListDomain(L), StringRange(ZERO, ListLength(L)))

axiom_list_compose = Equals(ListCompose(List(S), T), Subscript(S, T))
axiom_list_compose_list = Equals(ListCompose(List(S), List(T)), List(Subscript(S, T)))
axiom_list_compose_list_1 = Equals(ListCompose(L, List(S)), List(ListCompose(L, S)))
axiom_list_compose_set = Equals(ListCompose(L, Set(A)), Set(ListCompose(L, A)))

axiom_list_compose_associative = Equals(
    ListCompose(ListCompose(L, M), N), ListCompose(L, ListCompose(M, N))
)

axiom_list_at_base = Equals(ListAt(L, NIL), L)
axiom_list_at_singular = Equals(Length(i), ONE) >> Equals(
    ListAt(L, i), ListCompose(L, i)
)
axiom_list_at_string = Equals(ListAt(L, Join(S, T)), ListAt(ListAt(L, S), T))
axiom_list_replace_string = Equals(
    ListReplace(Join(S, T), i, L), ListReplace(S, ListReplace(T, i, ListAt(L, S)), L)
)
