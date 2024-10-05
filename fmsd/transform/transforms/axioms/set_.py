from fmsd.expression.operators.bunch import (
    Count,
    In as BunchIn,
    Union as BunchUnion,
    Intersect as BunchIntersect,
)
from fmsd.expression.operators.generic import NotEquals, Equals
from fmsd.expression.operators.set_ import (
    Set,
    Contents,
    Union,
    Intersect,
    Size,
    In,
    SubsetEq,
    Power,
)
from fmsd.expression.variables import SetVariable, NumericVariable
from fmsd.expression.types import Type

S = SetVariable("S", Type.NUMERIC)
A = NumericVariable("A")
B = NumericVariable("B")


axiom_structure = NotEquals(Set(A), A)
axiom_formation = Equals(Set(Contents(S)), S)
axiom_contents = Equals(Contents(Set(A)), A)
axiom_size = Equals(Size(Set(A)), Count(A))
axiom_elements = Equals(In(A, Set(B)), BunchIn(A, B))
axiom_subset = Equals(SubsetEq(Set(A), Set(B)), BunchIn(A, B))
axiom_power = Equals(BunchIn(Set(A), Power(B)), BunchIn(A, B))
axiom_union = Equals(Union(Set(A), Set(B)), Set(BunchUnion(A, B)))
axiom_intersection = Equals(Intersect(Set(A), Set(B)), Set(BunchIntersect(A, B)))
axiom_equation = Equals(Equals(Set(A), Set(B)), Equals(A, B))
