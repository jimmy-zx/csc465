from fmsd_impl.transforms.axioms import (
    numeric,
)
from fmsd_impl.transforms.axioms import (
    binary,
    bunch,
    numeric_generic,
    constants,
    binary_generic,
    context,
)
from fmsd.transform.transform import Transform
from fmsd_impl.transforms.expr import ExpressionTransform

modules = [
    binary,
    binary_generic,
    bunch,
    constants,
    context,
    numeric,
    numeric_generic,
]

t_all: dict[str, Transform] = {}

for mod in modules:
    for name in dir(mod):
        if not name.startswith("axiom_"):
            continue
        fqname = mod.__name__ + "::" + name
        t_all[fqname] = ExpressionTransform(getattr(mod, name))
        t_all[fqname].name = fqname
