from fmsd.ast import Node, VarNode
from fmsd.transform.transform import SymmetricFunctionTransform
from fmsd_impl.operators import Context, Function, FunctionCompose, In


@SymmetricFunctionTransform
def t_rename(src: Node, dst: Node) -> bool:
    if not isinstance(src, Function) and not isinstance(dst, Function):
        return False
    v = VarNode("v")
    w = VarNode("w")
    D = VarNode("D")
    b = VarNode("b")
    if (vt := Function(v, D, b).match(src, {})) is None:
        return False
    if (
        vt := Function(w, D, FunctionCompose(Function(v, D, b), w)).match(dst, vt)
    ) is None:
        return False
    for node in vt[D].walk_preorder():
        if node in (vt[v], vt[w]):
            return False
    for node in vt[b].walk_preorder():
        if node == vt[w]:
            return False
    return True


@SymmetricFunctionTransform
def t_application(src: Node, dst: Node) -> bool:
    v = VarNode("v")
    D = VarNode("D")
    b = VarNode("b")
    x = VarNode("x")
    if (
        vt := Context(FunctionCompose(Function(v, D, b), x), In(x, D)).match(src, {})
    ) is None:
        return False
    if vt[v] in vt[b].sym_decls():
        return False
    res = Context(vt[b].eval({vt[v]: vt[x]}), In(vt[x], vt[D]))
    return dst == res
