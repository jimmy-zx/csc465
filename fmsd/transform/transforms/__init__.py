import fmsd.transform.transforms.rule as rule

from fmsd.transform.prop import AssociativeTransform, CommutativeTransform

transforms = [
    AssociativeTransform(),
    CommutativeTransform(),
]

transforms.extend(rule.transforms)
