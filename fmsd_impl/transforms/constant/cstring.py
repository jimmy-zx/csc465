from fmsd.ast import Node
from fmsd.transform.transform import SymmetricFunctionTransform
from fmsd_impl.constants import to_natural
from fmsd_impl.operators import Join, Length, Replace, Subscript


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
    if len(dest_string) != 1 and not isinstance(dest_string, Join):
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
