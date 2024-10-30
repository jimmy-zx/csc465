from fmsd.transform.transform import Transform
from fmsd_impl.transforms.axioms import (
    binary,
    bunch,
    generic,
    constants,
    context,
    set_,
    string,
)
from fmsd_impl.transforms.axioms import (
    numeric,
)
from fmsd_impl.transforms.expr import ExpressionTransform

modules = [
    binary,
    bunch,
    constants,
    context,
    numeric,
    generic,
    set_,
    string,
]

t_all: dict[str, Transform] = {}

for mod in modules:
    for name in dir(mod):
        if not name.startswith("axiom_"):
            continue
        fqname = mod.__name__ + "::" + name
        t_all[fqname] = ExpressionTransform(getattr(mod, name))
        t_all[fqname].name = fqname
