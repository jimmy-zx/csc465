from fmsd.transform.transform import Transform
from fmsd_impl.transforms import axioms, prop
from fmsd_impl.transforms.constant import cbinary, clength, clist, cnatural, cstring

modules = [cbinary, prop, axioms, cnatural, clength, cstring, clist]

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

__all__ = ["t_all"]

if __name__ == "__main__":
    print("\n".join(t_all.keys()))
