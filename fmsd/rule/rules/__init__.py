import fmsd.rule.rules.table as table
import fmsd.rule.rules.generic as generic
import fmsd.rule.rules.binary as binary

rulelist = [table, generic, binary]

ruleset = {}

for module in rulelist:
    for rule_name in dir(module):
        if not rule_name.startswith("rule_"):
            continue
        rule = getattr(module, rule_name)
        if rule_name in ruleset:
            raise Exception(f"Duplicate rule {rule_name}: {ruleset[rule_name]}, {rule}")
        ruleset[rule_name] = rule
