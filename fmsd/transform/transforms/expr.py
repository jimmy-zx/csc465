from fmsd.rule import MatchRule
from fmsd.rule.rules import ruleset
from fmsd.transform.expr import ExpressionTransform

transforms = [
    ExpressionTransform(rule.to_expr(), rule.name) for rule in ruleset.values() if isinstance(rule, MatchRule)
]
