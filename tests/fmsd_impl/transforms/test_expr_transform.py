import pytest

from fmsd.ast import VarNode
from fmsd_impl.constants import INFINITY, ZERO
from fmsd_impl.operators import Context
from fmsd_impl.operators.binary import Implies
from fmsd_impl.operators.generic import Equals
from fmsd_impl.transforms.axioms import t_all
from fmsd_impl.transforms.axioms.numeric import axiom_inverse
from fmsd_impl.transforms.expr import ExpressionTransform


@pytest.mark.parametrize("transform", t_all.values(), ids=lambda t: t.name)
def test_match_rule_transform(transform):
    if not isinstance(transform, ExpressionTransform):
        pytest.skip()
    if isinstance(transform.expr, (Equals, Implies)):
        src = transform.expr.nodes[0]
        dst = transform.expr.nodes[1]
        assert transform.verify(src, dst)
    if isinstance(transform.expr, Equals):
        src = transform.expr.nodes[1]
        dst = transform.expr.nodes[0]
        assert transform.verify(src, dst)


def test_implied_context():
    x = VarNode("x")
    assert ExpressionTransform(axiom_inverse).verify(
        Context(x - x, (-INFINITY < x) & (x < INFINITY)),
        Context(ZERO, (-INFINITY < x) & (x < INFINITY)),
    )
