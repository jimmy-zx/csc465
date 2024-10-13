from fmsd.rule import FunctionRule
from fmsd.rule.rules import ruleset
from fmsd.transform.rule import RuleTransform

transforms = [
    RuleTransform(rule) for rule in ruleset.values() if isinstance(rule, FunctionRule)
]