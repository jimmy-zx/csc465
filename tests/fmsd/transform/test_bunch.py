from fmsd.ast.node import Variable
from fmsd_impl.constants.basic import NAT, TRUE, ZERO
from fmsd_impl.operators.bunch import In, Union
from fmsd_impl.transforms.axioms.bunch import axiom_generalization
from fmsd_impl.transforms.expr import ExpressionTransform


def test_generalization():
    n = Variable("n")
    assert ExpressionTransform(axiom_generalization).verify(
        TRUE, In(n * ZERO, Union(n * ZERO, n * NAT))
    )
