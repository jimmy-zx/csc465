import pytest

from fmsd.rule import MatchRule
from fmsd.rule.rules import ruleset


@pytest.mark.parametrize("rule_name", ruleset)
def test_match_rule(rule_name):
    rule = ruleset[rule_name]
    if not isinstance(rule, MatchRule):
        pytest.skip()
    orig = rule.pattern.copy()
    target = rule.repl.copy()
    assert rule(orig) == target