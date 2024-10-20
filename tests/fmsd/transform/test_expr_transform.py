import pytest

from fmsd.expression.operators.binary import Implies
from fmsd.expression.operators.generic import Equals
from fmsd.transform.expr import ExpressionTransform
from fmsd.transform.transforms import t_all


@pytest.mark.parametrize("transform", t_all.values(), ids=lambda t: t.name)
def test_match_rule_transform(transform):
    if not isinstance(transform, ExpressionTransform):
        pytest.skip()
    if isinstance(transform.expr, (Equals, Implies)):
        src = transform.expr.lhs.copy()
        dst = transform.expr.rhs.copy()
        assert transform.verify(src, dst)
    if isinstance(transform.expr, Equals):
        src = transform.expr.rhs.copy()
        dst = transform.expr.lhs.copy()
        assert transform.verify(src, dst)
