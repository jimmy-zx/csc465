from fmsd.ast import Variable
from fmsd_impl.operators import (
    Set,
    Contents,
    SetIn,
    SetIntersect,
    SetUnion,
    SubsetEq,
    Size,
    SetPower,
    Equals,
    NotEquals,
    In,
    Count,
    Union,
    Intersect,
)

S = Variable("S")
A = Variable("A")
B = Variable("B")

axiom_structure = NotEquals(Set(A), A)
axiom_formation = Equals(Set(Contents(S)), S)
axiom_contents = Equals(Contents(Set(A)), A)
axiom_size = Equals(Size(Set(A)), Count(A))
axiom_elements = Equals(SetIn(A, Set(B)), In(A, B))
axiom_subset = Equals(SubsetEq(Set(A), Set(B)), In(A, B))
axiom_power = Equals(In(Set(A), SetPower(B)), In(A, B))
axiom_union = Equals(SetUnion(Set(A), Set(B)), Set(Union(A, B)))
axiom_intersection = Equals(SetIntersect(Set(A), Set(B)), Set(Intersect(A, B)))
axiom_equation = Equals(Equals(Set(A), Set(B)), Equals(A, B))
