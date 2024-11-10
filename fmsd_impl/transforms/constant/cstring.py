from fmsd.ast import Node, Variable
from fmsd.transform.transform import SymmetricFunctionTransform
from fmsd_impl.constants import NIL
from fmsd_impl.operators import Join, Length, Replace, StringRange, Subscript
from fmsd_impl.transforms.ctype import to_natural


@SymmetricFunctionTransform
def t_subscript(src: Node, dst: Node) -> bool:
    """
    Simplified constant subscription.

    Alternative to `test_index_string`
    """
    if not isinstance(src, Subscript):
        return False
    source_string = src.nodes[0].flatten()
    index = src.nodes[1]
    if (n := to_natural(index)) is not None:
        return dst == source_string[n]
    if isinstance(index, Join) and isinstance(dst, Join):
        res: list[Node] = []
        for index_elem in index.flatten():
            if (n := to_natural(index_elem)) is None:
                return False
            if n >= len(source_string):
                return False
            res.append(source_string[n])
        return dst.flatten() == res
    return False


@SymmetricFunctionTransform
def t_replace(src: Node, dst: Node) -> bool:
    if not isinstance(src, Replace):
        return False
    source_string = src.nodes[0].flatten()
    index = src.nodes[1]
    if (n := to_natural(index)) is None:
        return False
    if n >= len(source_string):
        return False
    dest_string = dst.flatten()
    if len(dest_string) != 1 and not isinstance(dst, Join):
        return False
    source_string[n] = src.nodes[2]
    return source_string == dest_string


@SymmetricFunctionTransform
def t_length(src: Node, dst: Node) -> bool:
    if not isinstance(src, Length):
        return False
    if (l := to_natural(dst)) is None:
        return False
    if not isinstance(src.nodes[0], Join):
        return l == 1
    return len(src.nodes[0].flatten()) == l


@SymmetricFunctionTransform
def t_range(src: Node, dst: Node) -> bool:
    l = Variable("l")
    r = Variable("r")
    if (vt := StringRange(l, r).match(src, {})) is None:
        return False
    if not (lv := to_natural(vt["l"])):
        return False
    if not (rv := to_natural(vt["r"])):
        return False
    if lv == rv:
        return dst == NIL
    if lv + 1 == rv:
        return to_natural(dst) == lv
    if not isinstance(dst, Join):
        return False
    lst = dst.flatten()
    for elem in lst:
        if (v := to_natural(elem)) is None:
            return False
        if not lv <= v < rv:
            return False
    if len(set(lst)) != rv - lv:
        return False
    return True
