import pytest

from fmsd_impl.operators.binary import Implies
from fmsd_impl.operators.generic import Equals
from fmsd.transform.expr import ExpressionTransform
from fmsd.transform.transforms import t_all


@pytest.mark.parametrize("transform", t_all.values(), ids=lambda t: t.name)
def test_match_rule_transform(transform):
    if not isinstance(transform, ExpressionTransform):
        pytest.skip()
    if isinstance(transform.expr, (Equals, Implies)):
        src = transform.expr.nodes[0].copy()
        dst = transform.expr.nodes[1].copy()
        assert transform.verify(src, dst)
    if isinstance(transform.expr, Equals):
        src = transform.expr.nodes[1].copy()
        dst = transform.expr.nodes[0].copy()
        assert transform.verify(src, dst)
