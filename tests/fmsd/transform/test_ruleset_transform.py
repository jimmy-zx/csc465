import pytest

from fmsd.rule import MatchRule
from fmsd.transform.rule import RuleTransform
from fmsd.transform.transforms.rule import transforms


@pytest.mark.parametrize("transform", transforms)
def test_match_rule_transform(transform):
    if not isinstance(transform, RuleTransform):
        pytest.skip()
    rule = transform.rule
    if not isinstance(rule, MatchRule):
        pytest.skip()
    orig = rule.pattern.copy()
    target = rule.repl.copy()
    assert transform.verify(orig, target)
