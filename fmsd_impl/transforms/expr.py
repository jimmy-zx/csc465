from fmsd.ast.node import Node, VarTable
from fmsd.transform.transform import Transform
from fmsd_impl.constants import TRUE
from fmsd_impl.operators import Context, Equals, ImpliedBy, Implies


class ExpressionTransform(Transform):
    def __init__(self, expr: Node, *args, **kw) -> None:
        super().__init__(*args, **kw)
        assert isinstance(expr, Node)
        self.expr = expr

    def verify(self, src: Node, dst: Node) -> bool:
        return self.verify_once(src, dst, self.expr, {})

    @staticmethod
    def verify_once(src: Node, dst: Node, expr: Node, vt: VarTable) -> bool:
        if ExpressionTransform.verify_as_axiom(src, dst, expr, vt):
            return True
        if ExpressionTransform.verify_implies(src, dst, expr, vt):
            return True
        if ExpressionTransform.verify_equals(src, dst, expr, vt):
            return True
        if ExpressionTransform.verify_context(src, dst, expr, vt):
            return True
        return False

    @staticmethod
    def verify_context(src: Node, dst: Node, expr: Node, vt: VarTable) -> bool:
        """
        axiom = cond >> axiom1
        src = Context(src1, cond)
        dst = Context(dst1, cond)
        axiom1.verify(src1, dst1)
        """
        if (
            isinstance(expr, Implies)
            and isinstance(src, Context)
            and isinstance(dst, Context)
        ):
            if (m := expr.nodes[0].match(src.nodes[1], vt.copy())) is None:
                return False
            if src.nodes[1] != dst.nodes[1]:
                return False
            return ExpressionTransform.verify_once(
                src.nodes[0], dst.nodes[0], expr.nodes[1], m
            )
        return False

    @staticmethod
    def verify_as_axiom(src: Node, dst: Node, expr: Node, vt: VarTable) -> bool:
        """
        TRUE >>> axiom
        """
        if src == TRUE and expr.match(dst, vt.copy()) is not None:
            return True
        return False

    @staticmethod
    def verify_implies(src: Node, dst: Node, expr: Node, vt: VarTable) -> bool:
        """
        axiom = (left) >> (right)
        left >>> right
        """
        if isinstance(expr, (Equals, Implies)):
            if (m := expr.nodes[0].match(src, vt.copy())) is not None:
                if expr.nodes[1].match(dst, m) == m:
                    return True
        return False

    @staticmethod
    def verify_equals(src: Node, dst: Node, expr: Node, vt: VarTable) -> bool:
        """
        axiom = (left) << (right)
        right >>> left
        """
        if isinstance(expr, (Equals, ImpliedBy)):
            if (m := expr.nodes[1].match(src, vt.copy())) is not None:
                if expr.nodes[0].match(dst, m) == m:
                    return True
        return False

    def __eq__(self, other) -> bool:
        if not isinstance(other, ExpressionTransform):
            return False
        return self.expr == other.expr

    def __hash__(self):
        return hash((type(self), self.expr))
