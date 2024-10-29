from fmsd.ast.node import Node
from fmsd.transform.transform import Transform
from fmsd_impl.constants.basic import TRUE
from fmsd_impl.operators.generic import Equals
from fmsd_impl.operators.binary import Implies


class ExpressionTransform(Transform):
    def __init__(self, expr: Node) -> None:
        Transform.__init__(self)
        self.expr = expr

    def verify(self, src: Node, dst: Node) -> bool:
        if dst == TRUE and self.expr.match(src, {}) is not None:
            return True
        if src == TRUE and self.expr.match(dst, {}) is not None:
            return True
        if isinstance(self.expr, (Equals, Implies)):
            if (m := self.expr.nodes[0].match(src, {})) is not None:
                if self.expr.nodes[1].match(dst, m) == m:
                    return True
        if isinstance(self.expr, Equals):
            if (m := self.expr.nodes[1].match(src, {})) is not None:
                if self.expr.nodes[0].match(dst, m) == m:
                    return True
        return False

    def __eq__(self, other) -> bool:
        if not isinstance(other, ExpressionTransform):
            return False
        return self.expr == other.expr
