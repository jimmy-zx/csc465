import fmsd.rule.rules.binary as binary
import fmsd.rule.rules.generic as generic
import fmsd.rule.rules.table as table
from fmsd.rule import Rule

rulelist = [table, generic, binary]

ruleset: dict[str, Rule] = {}

for module in rulelist:
    for rule_name in dir(module):
        if not rule_name.startswith("rule_"):
            continue
        rule = getattr(module, rule_name)
        rule.name = rule_name.replace("rule_", "", 1)
        if rule_name in ruleset:
            raise Exception(f"Duplicate rule {rule_name}: {ruleset[rule_name]}, {rule}")
        ruleset[rule_name] = rule
