import fmsd.rule.rules.binary as binary
import fmsd.rule.rules.binary.generic as binary_generic
import fmsd.rule.rules.binary.table as binary_table
import fmsd.rule.rules.numeric as numeric
import fmsd.rule.rules.numeric.generic as numeric_generic
from fmsd.rule import Rule

rulelist = [binary_table, binary_generic, binary, numeric, numeric_generic]

ruleset: dict[str, Rule] = {}

for module in rulelist:
    for rule_name in dir(module):
        if not rule_name.startswith("rule_"):
            continue
        rule = getattr(module, rule_name)
        rule.name = module.__name__ + "." + rule_name.replace("rule_", "", 1)
        if rule.name in ruleset:
            raise Exception(f"Duplicate rule {rule.name}")
        ruleset[rule.name] = rule
