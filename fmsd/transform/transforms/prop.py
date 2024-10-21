from fmsd.expression import Expression
from fmsd.expression.operators import AssociativeOperator, CommutativeOperator
from fmsd.transform.func import FunctionTransform


def func_associative(src: Expression, dst: Expression) -> bool:
    if type(src) != type(dst):
        return False
    if not isinstance(src, AssociativeOperator):
        return False
    if not isinstance(src, CommutativeOperator):
        return src.collect() == dst.collect()
    return set(src.collect()) == set(dst.collect())


t_associative = FunctionTransform(func_associative)


def func_commutative(src: Expression, dst: Expression) -> bool:
    if type(src) != type(dst):
        return False
    if not isinstance(src, CommutativeOperator):
        return False
    return set(src.children) == set(dst.children)


t_commutative = FunctionTransform(func_commutative)
