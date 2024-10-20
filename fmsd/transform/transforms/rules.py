from fmsd.rule import MatchRule
from fmsd.rule.rules import ruleset
from fmsd.transform import Transform
from fmsd.transform.expr import ExpressionTransform

t_all: dict[str, Transform] = {}

for name, rule in ruleset.items():
    assert isinstance(rule, MatchRule)
    t_all[name] = ExpressionTransform(rule.to_expr())
