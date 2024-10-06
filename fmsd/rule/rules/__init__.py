from typing import Callable
import fmsd.rule.rules.table as table
import fmsd.rule.rules.generic as generic
import fmsd.rule.rules.binary as binary
from fmsd.expression import Expression, VarTable

rulelist = [table, generic, binary]

ruleset: dict[str, Callable[[Expression, VarTable], Expression]] = {}

for module in rulelist:
    for rule_name in dir(module):
        if not rule_name.startswith("rule_"):
            continue
        rule = getattr(module, rule_name)
        print(rule)
        if rule_name in ruleset:
            raise Exception(f"Duplicate rule {rule_name}: {ruleset[rule_name]}, {rule}")
        ruleset[rule_name] = rule
