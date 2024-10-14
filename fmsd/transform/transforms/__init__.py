import fmsd.transform.transforms.rule as rule
import fmsd.transform.transforms.expr as expr
import fmsd.transform.transforms.axioms as axioms

from fmsd.transform.prop import AssociativeTransform, CommutativeTransform

transforms = [
    AssociativeTransform(),
    CommutativeTransform(),
]

transforms.extend(rule.transforms)
transforms.extend(expr.transforms)
transforms.extend(axioms.transforms)
