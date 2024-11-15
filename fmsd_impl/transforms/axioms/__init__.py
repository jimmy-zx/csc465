from fmsd.transform.transform import Transform
from fmsd_impl.transforms.axioms import (
    binary,
    bunch,
    constants,
    context,
    function,
    generic,
    list_,
    numeric,
    quantifier,
    set_,
    string_,
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
    string_,
    list_,
    function,
    quantifier,
]

t_all: dict[str, Transform] = {}

for mod in modules:
    for name in dir(mod):
        if not name.startswith("axiom_"):
            continue
        fqname = mod.__name__ + "::" + name
        try:
            t_all[fqname] = ExpressionTransform(getattr(mod, name))
        except Exception as ex:
            raise ValueError(
                f"Invalid expression {fqname}: {getattr(mod, name)}"
            ) from ex
        t_all[fqname].name = fqname
