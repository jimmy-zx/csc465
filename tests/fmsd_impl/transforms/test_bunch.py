from fmsd.ast.node import VarNode
from fmsd.impl.transforms import ExpressionTransform
from fmsd_impl.constants.basic import NAT, TRUE, ZERO
from fmsd_impl.operators.bunch import In, Union
from fmsd_impl.transforms.axioms.bunch import axiom_generalization


def test_generalization():
    n = VarNode("n")
    assert ExpressionTransform(axiom_generalization).verify(
        TRUE, In(n * ZERO, Union(n * ZERO, n * NAT))
    )
