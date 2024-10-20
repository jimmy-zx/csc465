import fmsd.transform.transforms.axioms.bunch as bunch
import fmsd.transform.transforms.axioms.constants as constants
import fmsd.transform.transforms.axioms.context as context
from fmsd.transform import Transform
from fmsd.transform.expr import ExpressionTransform

modules = [bunch, constants, context]

t_all: dict[str, Transform] = {}

for mod in modules:
    for name in dir(mod):
        if not name.startswith("axiom_"):
            continue
        fqname = mod.__name__ + "::" + name
        t_all[fqname] = ExpressionTransform(getattr(mod, name))
        t_all[fqname].name = fqname
