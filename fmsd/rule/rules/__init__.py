from fmsd.rule.rules import binary
from fmsd.rule.rules import numeric
from fmsd.rule.rules.binary import generic as binary_generic
from fmsd.rule.rules.numeric import generic as numeric_generic
from fmsd.transform import Transform
from fmsd.transform.expr import ExpressionTransform

modules = [
    binary,
    binary_generic,
    numeric,
    numeric_generic,
]

t_all: dict[str, Transform] = {}

for mod in modules:
    for name in dir(mod):
        if not name.startswith("rule_"):
            continue
        fqname = mod.__name__ + "::" + name
        t_all[fqname] = ExpressionTransform(getattr(mod, name))
        t_all[fqname].name = name
