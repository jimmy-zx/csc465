from collections import deque

from fmsd.ast import Node
from fmsd.transform.transform import SymmetricFunctionTransform
from fmsd_impl.operators import Join, ListAt
from fmsd_impl.transforms.ctype import to_list, to_natural


@SymmetricFunctionTransform
def t_at(src: Node, dst: Node) -> bool:
    if not isinstance(src, ListAt):
        return False
    lst = to_list(src.nodes[0])
    node_index = src.nodes[1]
    idx: deque[int]
    if isinstance(node_index, Join):
        idx = deque()
        for node in node_index.flatten():
            if (v := to_natural(node)) is None:
                return False
            idx.append(v)
    else:
        if (v := to_natural(node_index)) is None:
            return False
        idx = deque([v])
    while idx:
        if isinstance(lst, list) and idx[0] < len(lst):
            lst = lst[idx.popleft()]
        else:
            return False
    return lst == to_list(dst)


__all__ = [
    "t_at",
]
