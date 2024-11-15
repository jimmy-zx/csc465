import fmsd_impl.patch
from fmsd.ast import VarNode
from fmsd_impl.constants import NULL
from fmsd_impl.operators import (
    Context,
    Equals,
    Exists,
    Forall,
    Function,
    FunctionCompose,
    FunctionDomain,
    FunctionSize,
    FunctionTo,
    FunctionUnion,
    In,
    Intersect,
    Size,
    Solution,
    Ternary,
    Union,
)

assert fmsd_impl.patch

A = VarNode("A")
B = VarNode("B")
f = VarNode("f")
g = VarNode("g")
h = VarNode("h")
x = VarNode("x")
y = VarNode("y")
v = VarNode("v")
b = VarNode("b")
D = VarNode("D")

axiom_composition_associative = Equals(
    FunctionCompose(FunctionCompose(g, f), x),
    FunctionCompose(g, FunctionCompose(f, x)),
)
axiom_domain = Equals(FunctionDomain(Function(v, D, b)), D)

axiom_union_domain = Equals(
    FunctionDomain(Union(f, g)), Intersect(FunctionDomain(f), FunctionDomain(g))
)
axiom_union_eval = Equals(
    FunctionCompose(Union(f, g), x), Union(FunctionCompose(f, x), FunctionCompose(g, x))
)

axiom_intersection_domain = Equals(
    FunctionDomain(Intersect(f, g)), Union(FunctionDomain(f), FunctionDomain(g))
)
axiom_intersection_eval = Equals(
    FunctionCompose(Intersect(f, g), x),
    Intersect(
        FunctionCompose(FunctionUnion(f, g), x), FunctionCompose(FunctionUnion(g, f), x)
    ),
)

axiom_selective_union_domain = Equals(
    FunctionDomain(FunctionUnion(f, g)), Union(FunctionDomain(f), FunctionDomain(g))
)
axiom_selective_union_eval = Equals(
    FunctionCompose(FunctionUnion(f, g), x),
    Ternary(In(x, FunctionDomain(f)), FunctionCompose(f, x), FunctionCompose(g, x)),
)
axiom_selective_union_base = Equals(FunctionUnion(f, f), f)
axiom_selective_union_associative = Equals(
    FunctionUnion(f, FunctionUnion(g, h)), FunctionUnion(FunctionUnion(f, g), h)
)
axiom_selective_union_compose = Equals(
    FunctionCompose(FunctionUnion(g, h), f),
    FunctionUnion(FunctionCompose(g, f), FunctionCompose(h, f)),
)

axiom_bunch_null = Equals(FunctionCompose(f, NULL), NULL)
axiom_bunch = Equals(
    FunctionCompose(f, Union(A, B)), Union(FunctionCompose(f, A), FunctionCompose(f, B))
)
axiom_solution = Equals(
    FunctionCompose(f, Solution(g)),
    Solution(
        Function(
            y,
            FunctionCompose(f, FunctionDomain(g)),
            Exists(
                Function(
                    x,
                    FunctionDomain(g),
                    Equals(FunctionCompose(f, x), y) & FunctionCompose(g, x),
                )
            ),
        )
    ),
)
axiom_ternary_op = Equals(
    FunctionCompose(f, Ternary(b, x, y)),
    Ternary(b, FunctionCompose(f, x), FunctionCompose(f, y)),
)
axiom_ternary_func = Equals(
    FunctionCompose(Ternary(b, f, g), x),
    Ternary(b, FunctionCompose(f, x), FunctionCompose(g, x)),
)

axiom_size = Equals(FunctionSize(f), Size(FunctionDomain(f)))

axiom_equality = Equals(
    Equals(f, g),
    Equals(FunctionDomain(f), FunctionDomain(g))
    & Forall(
        Function(
            x, FunctionDomain(f), Equals(FunctionCompose(f, x), FunctionCompose(g, x))
        )
    ),
)
axiom_inclusion = Equals(
    In(f, g),
    In(FunctionDomain(g), FunctionDomain(f))
    & Forall(
        Function(x, FunctionDomain(g), In(FunctionCompose(f, x), FunctionCompose(g, x)))
    ),
)
axiom_inclusion_to = Equals(
    In(f, FunctionTo(A, B)), In(A, FunctionDomain(f)) & In(FunctionCompose(f, A), B)
)

axiom_extension = Equals(f, Function(v, FunctionDomain(f), FunctionCompose(f, v)))

axiom_to = Equals(FunctionTo(D, b), Function(x, D, b))

axiom_function_domain_context = Equals(
    Function(v, D, b), Function(v, D, Context(b, In(v, D)))
)
