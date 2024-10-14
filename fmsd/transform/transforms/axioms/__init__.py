import fmsd.transform.transforms.axioms.bunch as bunch
import fmsd.transform.transforms.axioms.constants as constants
import fmsd.transform.transforms.axioms.context as context
from fmsd.transform.expr import ExpressionTransform

modules = [bunch, constants, context]

transforms = []

for module in modules:
    for axiom in dir(module):
        if not axiom.startswith("axiom_"):
            continue
        transforms.append(ExpressionTransform(getattr(module, axiom), axiom))
