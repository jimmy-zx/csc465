import fmsd.transform.transforms.axioms.bunch as bunch
from fmsd.transform.expr import ExpressionTransform

modules = [bunch]

transforms = []

for module in modules:
    for axiom in dir(module):
        if not axiom.startswith("axiom_"):
            continue
        transforms.append(ExpressionTransform(getattr(module, axiom), axiom))
