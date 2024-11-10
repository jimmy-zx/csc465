from fmsd.ast import Node, Variable
from fmsd.transform.transform import SymmetricFunctionTransform
from fmsd_impl.constants import FALSE, INFINITY, ONE, TRUE, ZERO
from fmsd_impl.operators import (
    And,
    Equals,
    ImpliedBy,
    Implies,
    Length,
    Max,
    Min,
    Minus,
    Multiply,
    NotEquals,
    Or,
    Plus,
)
from fmsd_impl.transforms.ctype import to_natural


@SymmetricFunctionTransform
def t_constant_length(src: Node, dst: Node) -> bool:
    if src != TRUE:
        return False
    x = Variable("x")
    y = Variable("y")
    if (vt := Equals(Length(x), y).match(dst, {})) is None:
        return False
    if vt["y"] == ONE and (
        vt["x"] in {TRUE, FALSE, ZERO, ONE, INFINITY} or to_natural(vt["x"]) is not None
    ):
        return True
    return False


@SymmetricFunctionTransform
def t_unit_length(src: Node, dst: Node) -> bool:
    if dst != TRUE:
        return False
    x = Variable("x")
    y = Variable("y")
    r = Variable("r")
    if (
        vt := (
            (Equals(Length(x), ONE) & Equals(Length(y), ONE)) >> Equals(Length(r), ONE)
        ).match(src, {})
    ) is None:
        return False
    if len(vt["r"].nodes) != 2:
        return False
    if set(vt["r"].nodes) != {vt["x"], vt["y"]}:
        return False
    if not isinstance(
        vt["r"],
        (
            And,
            Or,
            Implies,
            ImpliedBy,
            Equals,
            NotEquals,
            Plus,
            Minus,
            Multiply,
            Min,
            Max,
        ),
    ):
        return False
    return True
