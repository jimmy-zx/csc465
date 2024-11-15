import fmsd_impl.patch
from fmsd.ast import Node, VarNode
from fmsd_impl.constants import FALSE, INFINITY, INT, NAT, NULL, ONE, REAL, TRUE, ZERO
from fmsd_impl.operators import (
    And,
    Count,
    Equals,
    Exists,
    Forall,
    Function,
    FunctionCompose,
    FunctionDomain,
    FunctionTo,
    GreaterThan,
    GreaterThanOrEqualsTo,
    Implies,
    In,
    Intersect,
    LessThan,
    LessThanOrEqualsTo,
    Max,
    Min,
    Minus,
    Multiply,
    NotEquals,
    Or,
    Plus,
    Power,
    Product,
    QMax,
    QMin,
    Solution,
    SubsetEq,
    Sum,
    Ternary,
    Union,
    VTCondition,
)
from fmsd_impl.transforms.conditions import symbol_notin

assert fmsd_impl.patch

v = VarNode("v")
w = VarNode("w")
x = VarNode("x")
y = VarNode("y")
a = VarNode("a")
b = VarNode("b")
c = VarNode("c")
f = VarNode("f")
p = VarNode("p")
g = VarNode("g")
A = VarNode("A")
B = VarNode("B")
D = VarNode("D")
n = VarNode("n")
m = VarNode("m")
k = VarNode("k")
r = VarNode("r")
d = VarNode("d")

vDb = Function(v, D, b)
vxb = Function(v, x, b)
vDbx = FunctionCompose(vDb, x)
vxbx = FunctionCompose(vxb, x)


# P240


def rule_generate(
    quantifier: type[Node], null: Node, base: Node, union: type[Node], solution: Node
) -> tuple[Node, Node, Node, Node]:
    return (
        Equals(quantifier(Function(v, NULL, b)), null),
        Equals(Count(x), ONE) >> Equals(quantifier(vxb), base),
        Equals(
            quantifier(Function(v, Union(A, B), b)),
            union(quantifier(Function(v, A, b)), quantifier(Function(v, B, b))),
        ),
        Equals(
            quantifier(Function(v, Solution(Function(w, D, FunctionCompose(f, w))), c)),
            quantifier(Function(v, D, solution)),
        ),
    )


axiom_forall_null, axiom_forall_base, axiom_forall_union, axiom_forall_solution = (
    rule_generate(
        Forall,
        TRUE,
        vxbx,
        And,
        Implies(FunctionCompose(f, v), c),
    )
)

axiom_exists_null, axiom_exists_base, axiom_exists_union, axiom_exists_solution = (
    rule_generate(
        Exists,
        FALSE,
        vxbx,
        Or,
        And(FunctionCompose(f, v), c),
    )
)

axiom_sum_null, axiom_sum_base, axiom_sum_union, axiom_sum_solution = rule_generate(
    Sum,
    ZERO,
    vxbx,
    Plus,
    Ternary(FunctionCompose(f, v), c, ZERO),
)

axiom_product_null, axiom_product_base, axiom_product_union, axiom_product_solution = (
    rule_generate(
        Product,
        ONE,
        vxbx,
        Multiply,
        Ternary(FunctionCompose(f, v), c, ONE),
    )
)

axiom_min_null, axiom_min_base, axiom_min_union, axiom_min_solution = rule_generate(
    QMin,
    INFINITY,
    vxbx,
    Min,
    Ternary(FunctionCompose(f, v), c, INFINITY),
)

axiom_max_null, axiom_max_base, axiom_max_union, axiom_max_solution = rule_generate(
    QMax,
    -INFINITY,
    vxbx,
    Max,
    Ternary(FunctionCompose(f, v), c, -INFINITY),
)

(
    axiom_solution_null,
    axiom_solution_base,
    axiom_solution_union,
    axiom_solution_solution,
) = rule_generate(
    Solution,
    NULL,
    Ternary(vxbx, x, NULL),
    Union,
    And(FunctionCompose(f, v), c),
)
axiom_solution_intersect = Equals(
    Solution(Function(v, Intersect(A, B), b)),
    Intersect(Solution(Function(v, A, b)), Solution(Function(v, B, b))),
)

axiom_inclusion = Equals(In(A, B), Forall(Function(x, A, In(x, B))))

axiom_cardinality = Equals(Count(A), Sum(FunctionTo(A, ONE)))

axiom_identity_forall = Forall(Function(v, D, TRUE))
axiom_identity_exists = ~Exists(Function(v, D, FALSE))

axiom_bunch_element_conversion = Equals(
    In(A, B), Forall(Function(a, A, Exists(Function(b, B, Equals(a, b)))))
)
axiom_bunch_element_conversion_func = Equals(
    In(FunctionCompose(f, A), FunctionCompose(g, B)),
    Forall(
        Function(
            a,
            A,
            Exists(
                Function(b, B, Equals(FunctionCompose(f, a), FunctionCompose(g, b)))
            ),
        )
    ),
)

axiom_range_min = Implies(In(x, FunctionDomain(f)), QMin(f) <= FunctionCompose(f, x))
axiom_range_max = Implies(In(x, FunctionDomain(f)), FunctionCompose(f, x) <= QMax(f))


def generate_change_of_variable(quantifier: type[Node]) -> Node:
    return VTCondition(
        Equals(
            quantifier(Function(r, FunctionCompose(f, D), b)),
            quantifier(
                Function(
                    d,
                    D,
                    FunctionCompose(
                        Function(r, FunctionCompose(f, D), b), FunctionCompose(f, d)
                    ),
                )
            ),
        ),
        symbol_notin(d, b),
    )


axiom_cov_forall = generate_change_of_variable(Forall)
axiom_cov_exists = generate_change_of_variable(Exists)
axiom_cov_min = generate_change_of_variable(QMin)
axiom_cov_max = generate_change_of_variable(QMax)


def generate_distributive(quantifier: type[Node], op: type[Node]) -> Node:
    return VTCondition(
        Equals(
            op(a, quantifier(Function(v, D, b))), quantifier(Function(v, D, op(a, b)))
        ),
        symbol_notin(v, a),
    )


axiom_distributive_forall_and = generate_distributive(Forall, And)
axiom_distributive_forall_or = generate_distributive(Forall, Or)
axiom_distributive_forall_implies = generate_distributive(Forall, Implies)
axiom_distributive_exists_and = generate_distributive(Exists, And)
axiom_distributive_exists_or = generate_distributive(Exists, Or)
axiom_distributive_exists_implies = generate_distributive(Exists, Implies)

axiom_idempotent_forall = VTCondition(
    Implies(Forall(Function(v, D, b)), b), symbol_notin(v, b)
)
axiom_idempotent_exists = VTCondition(
    Implies(Exists(Function(v, D, b)), b), symbol_notin(v, b)
)

# P241

axiom_absorption_and_exists = Implies(In(x, D), Equals(And(vDbx, Exists(vDb)), vDb))
axiom_absorption_or_forall = Implies(In(x, D), Equals(Or(vDbx, Forall(vDb)), vDb))
axiom_absorption_and_forall = Implies(
    In(x, D), Equals(And(vDbx, Forall(vDb)), Forall(vDb))
)
axiom_absorption_or_exists = Implies(
    In(x, D), Equals(Or(vDbx, Exists(vDb)), Exists(vDb))
)

axiom_antidistributive_exists = VTCondition(
    Implies(
        NotEquals(D, NULL),
        Equals(
            Implies(Exists(Function(v, D, b)), a),
            Forall(Function(v, D, Implies(b, a))),
        ),
    ),
    symbol_notin(v, a),
)
axiom_antidistributive_forall = VTCondition(
    Implies(
        NotEquals(D, NULL),
        Equals(
            Implies(Forall(Function(v, D, b)), a), Exists(Function(v, D, Implies(b, a)))
        ),
    ),
    symbol_notin(v, a),
)

axiom_specialization = Implies(
    In(x, FunctionDomain(p)), Implies(Forall(p), FunctionCompose(p, x))
)
axiom_generalization = Implies(
    In(x, FunctionDomain(p)), Implies(FunctionCompose(p, x), Exists(p))
)

axiom_one_point_forall = VTCondition(
    Implies(
        In(x, D),
        Equals(
            Forall(Function(v, D, Implies(Equals(v, x), b))),
            FunctionCompose(Function(v, D, b), x),
        ),
    ),
    symbol_notin(v, x),
)
axiom_one_point_exists = VTCondition(
    Implies(
        In(x, D),
        Equals(
            Exists(Function(v, D, And(Equals(v, x), b))),
            FunctionCompose(Function(v, D, b), x),
        ),
    ),
    symbol_notin(v, x),
)

axiom_duality_forall = Equals(~Forall(vDb), Exists(Function(v, D, ~b)))
axiom_duality_exists = Equals(~Exists(vDb), Forall(Function(v, D, ~b)))
axiom_duality_max = Equals(-QMax(vDb), QMin(Function(v, D, -b)))
axiom_duality_min = Equals(-QMin(vDb), QMax(Function(v, D, -b)))

axiom_splitting_forall_and = Equals(
    Forall(Function(v, D, a & b)), Forall(Function(v, D, a)) & Forall(Function(v, D, b))
)
axiom_splitting_exists_or = Equals(
    Exists(Function(v, D, a | b)), Exists(Function(v, D, a)) | Exists(Function(v, D, b))
)
axiom_splitting_forall_or = Implies(
    Forall(Function(v, D, a)) | Forall(Function(v, D, b)), Forall(Function(v, D, a | b))
)
axiom_splitting_exists_and = Implies(
    Exists(Function(v, D, a)) & Exists(Function(v, D, b)), Exists(Function(v, D, a & b))
)
axiom_splitting_implies_forall = Implies(
    Forall(Function(v, D, a >> b)),
    Forall(Function(v, D, a)) >> Forall(Function(v, D, b)),
)
axiom_splitting_implies_exists = Implies(
    Forall(Function(v, D, a >> b)),
    Exists(Function(v, D, a)) >> Exists(Function(v, D, b)),
)
axiom_splitting_equals_forall = Implies(
    Forall(Function(v, D, Equals(a, b))),
    Equals(Forall(Function(v, D, a)), Forall(Function(v, D, b))),
)
axiom_splitting_equals_exists = Implies(
    Forall(Function(v, D, Equals(a, b))),
    Equals(Exists(Function(v, D, a)), Exists(Function(v, D, b))),
)

axiom_commutative_forall = Equals(
    Forall(Function(v, A, Forall(Function(w, B, b)))),
    Forall(Function(w, B, Forall(Function(v, A, b)))),
)
axiom_commutative_exists = Equals(
    Exists(Function(v, A, Exists(Function(w, B, b)))),
    Exists(Function(w, B, Exists(Function(v, A, b)))),
)

axiom_semicommutative = Implies(
    Exists(Function(v, A, Forall(Function(w, B, b)))),
    Forall(Function(w, B, Exists(Function(v, A, b)))),
)
axiom_semicommutative_func = Equals(
    Forall(
        Function(
            v, A, Exists(Function(w, B, FunctionCompose(FunctionCompose(p, v), w)))
        )
    ),
    Exists(
        Function(
            f,
            FunctionTo(A, B),
            Forall(
                Function(
                    x, A, FunctionCompose(FunctionCompose(p, x), FunctionCompose(f, x))
                )
            ),
        )
    ),
)

axiom_solution_true = Equals(Solution(Function(v, D, TRUE)), D)
axiom_solution_domain = SubsetEq(Solution(Function(v, D, b)), D)
axiom_solution_false = Equals(Solution(Function(v, D, FALSE)), NULL)
axiom_solution_in = Equals(
    In(Solution(Function(v, D, b)), Solution(Function(v, D, c))),
    Forall(Function(v, D, b >> c)),
)
axiom_solution_union_cond = Equals(
    Union(Solution(Function(v, D, b)), Solution(Function(v, D, c))),
    Solution(Function(v, D, b | c)),
)
axiom_solution_intersect_cond = Equals(
    Intersect(Solution(Function(v, D, b)), Solution(Function(v, D, c))),
    Solution(Function(v, D, b & c)),
)
axiom_solution_element = Equals(
    In(x, Solution(p)), In(x, FunctionDomain(p)) & FunctionCompose(p, x)
)
axiom_solution_forall = Equals(Forall(f), Equals(Solution(f), FunctionDomain(f)))
axiom_solution_exists = Equals(Exists(f), NotEquals(Solution(f), NULL))

axiom_domain_change_forall = Implies(
    In(A, B), Implies(Forall(Function(v, B, b)), Forall(Function(v, A, b)))
)
axiom_domain_change_exists = Implies(
    In(A, B), Implies(Exists(Function(v, A, b)), Exists(Function(v, B, b)))
)
axiom_domain_change_intersect_forall = Equals(
    Forall(Function(v, A, Implies(In(v, B), p))),
    Forall(Function(v, Intersect(A, B), p)),
)
axiom_domain_change_intersect_exists = Equals(
    Exists(Function(v, A, And(In(v, B), p))), Exists(Function(v, Intersect(A, B), p))
)

axiom_extreme_min_int = Equals(QMin(Function(x, INT, x)), -INFINITY)
axiom_extreme_min_real = Equals(QMin(Function(x, REAL, x)), -INFINITY)
axiom_extreme_min_nat = Equals(QMin(Function(x, NAT, x)), ZERO)
axiom_extreme_max_int = Equals(QMax(Function(x, INT, x)), INFINITY)
axiom_extreme_max_real = Equals(QMax(Function(x, REAL, x)), INFINITY)
axiom_extreme_max_nat = Equals(QMax(Function(x, NAT, x)), INFINITY)

axiom_connection_le = Equals(n <= m, Forall(Function(k, D, (k <= n) >> (k <= m))))
axiom_connection_lt = Equals(n <= m, Forall(Function(k, D, (k < n) >> (k < m))))
axiom_connection_rle = Equals(n <= m, Forall(Function(k, D, (m <= k) >> (n <= k))))
axiom_connection_rlt = Equals(n <= m, Forall(Function(k, D, (m < k) >> (n < k))))


def generate_bounding(
    op: type[Node], lq: type[Node], conn: type[Node], rq: type[Node]
) -> Node:
    return VTCondition(
        Implies(
            NotEquals(D, NULL),
            conn(
                op(n, lq(Function(v, D, m))),
                rq(Function(v, D, op(n, m))),
            ),
        ),
        symbol_notin(v, n),
    )


def generate_bounding_rev(
    op: type[Node], lq: type[Node], conn: type[Node], rq: type[Node]
) -> Node:
    return VTCondition(
        Implies(
            NotEquals(D, NULL),
            conn(
                rq(Function(v, D, op(n, m))),
                op(n, lq(Function(v, D, m))),
            ),
        ),
        symbol_notin(v, n),
    )


axiom_bounding_gt_max = generate_bounding(GreaterThan, QMax, Implies, Forall)
axiom_bounding_lt_min = generate_bounding(LessThan, QMin, Implies, Forall)
axiom_bounding_ge_max = generate_bounding(GreaterThanOrEqualsTo, QMax, Equals, Forall)
axiom_bounding_le_min = generate_bounding(LessThanOrEqualsTo, QMin, Equals, Forall)
axiom_bounding_gt_min = generate_bounding(GreaterThan, QMin, Equals, Exists)
axiom_bounding_lt_max = generate_bounding(LessThan, QMax, Equals, Exists)
axiom_bounding_ge_min = generate_bounding_rev(
    GreaterThanOrEqualsTo, QMin, Implies, Exists
)
axiom_bounding_le_max = generate_bounding_rev(LessThanOrEqualsTo, QMax, Implies, Exists)


def generate_distributive_left(outer: type[Node], inner: type[Node]) -> Node:
    return VTCondition(
        Implies(
            NotEquals(D, NULL),
            Equals(
                outer(n, inner(Function(v, D, m))), inner(Function(v, D, outer(n, m)))
            ),
        ),
        symbol_notin(v, n),
    )


def generate_distributive_left_cond(
    cond: Node, outer: type[Node], inner: type[Node], inner1: type[Node] | None = None
) -> Node:
    inner1 = inner1 or inner
    return VTCondition(
        Implies(
            NotEquals(D, NULL),
            Implies(
                cond,
                Equals(
                    outer(n, inner(Function(v, D, m))),
                    inner1(Function(v, D, outer(n, m))),
                ),
            ),
        ),
        symbol_notin(v, n),
    )


def generate_distributive_right(outer: type[Node], inner: type[Node]) -> Node:
    return VTCondition(
        Implies(
            NotEquals(D, NULL),
            Equals(
                outer(inner(Function(v, D, m)), n), inner(Function(v, D, outer(m, n)))
            ),
        ),
        symbol_notin(v, n),
    )


axiom_distributive_max_max = generate_distributive_left(Max, QMax)
axiom_distributive_max_min = generate_distributive_left(Max, QMin)
axiom_distributive_min_min = generate_distributive_left(Min, QMin)
axiom_distributive_min_max = generate_distributive_left(Min, QMax)
axiom_distributive_plus_max = generate_distributive_left(Plus, QMax)
axiom_distributive_minus_max = generate_distributive_left(Minus, QMax)
axiom_distributive_plus_min = generate_distributive_left(Plus, QMin)
axiom_distributive_minus_min = generate_distributive_left(Minus, QMin)
axiom_distributive_right_minus_max = generate_distributive_right(Minus, QMax)
axiom_distributive_right_minus_min = generate_distributive_right(Minus, QMin)
axiom_distributive_mult_max_pos = generate_distributive_left_cond(
    n >= ZERO, Multiply, QMax
)
axiom_distributive_mult_min_pos = generate_distributive_left_cond(
    n >= ZERO, Multiply, QMin
)
axiom_distributive_mult_max_neg = generate_distributive_left_cond(
    n <= ZERO, Multiply, QMax, QMin
)
axiom_distributive_mult_min_neg = generate_distributive_left_cond(
    n <= ZERO, Multiply, QMax, QMin
)

axiom_distributive_mult_sum = generate_distributive_left(Multiply, Sum)

axiom_distributive_power_prod = generate_distributive_right(Power, Product)
