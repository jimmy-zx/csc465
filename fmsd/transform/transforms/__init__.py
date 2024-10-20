import fmsd.transform.transforms.axioms as axioms
import fmsd.transform.transforms.binary_table as binary_table
import fmsd.transform.transforms.prop as prop
import fmsd.transform.transforms.rules as rules
from fmsd.transform import Transform

modules = [
    binary_table,
    prop,
    axioms,
    rules
]

t_all: dict[str, Transform] = {}

for mod in modules:
    if (a := getattr(mod, "t_all", None)) is not None:
        t_all.update(a)
        continue
    for name in dir(mod):
        if not name.startswith("t_"):
            continue
        fqname = mod.__name__ + "::" + name
        t_all[fqname] = getattr(mod, name)
        t_all[fqname].name = fqname


if __name__ == '__main__':
    print("\n".join(t_all.keys()))
