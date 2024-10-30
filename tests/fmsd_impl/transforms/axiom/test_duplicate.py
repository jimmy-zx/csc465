import fmsd_impl.transforms.axioms
from fmsd_impl.transforms.expr import ExpressionTransform


def test_duplicate_axiom():
    t_all = fmsd_impl.transforms.axioms.t_all
    duplicate_pairs = []
    for lkey, lval in t_all.items():
        assert isinstance(lval, ExpressionTransform)
        for rkey, rval in t_all.items():
            assert isinstance(rval, ExpressionTransform)
            if lval.expr == rval.expr and lkey < rkey:
                duplicate_pairs.append((lkey, rkey))
    assert not duplicate_pairs, "\n".join(map(str, duplicate_pairs))
