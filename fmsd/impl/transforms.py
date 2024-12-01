from fmsd.ast.node import Node, VarTable
from fmsd.impl.constants import TRUE
from fmsd.impl.operators import Context, Equals, Implies, VTCondition
from fmsd.transform.transform import Transform


class ExpressionTransform(Transform):
    def __init__(self, expr: Node, *args, **kw) -> None:
        super().__init__(*args, **kw)
        assert isinstance(expr, Node)
        self.expr = expr

    def verify(self, src: Node, dst: Node) -> bool:
        expr = self.expr
        cond = None
        if isinstance(expr, VTCondition):
            cond = expr.meta["cond"]
            expr = expr.nodes[0]
        if (m := self.verify_once(src, dst, expr, {})) is None:
            return False
        return cond is None or cond(m)

    @staticmethod
    def verify_once(src: Node, dst: Node, expr: Node, vt: VarTable) -> VarTable | None:
        if (m := ExpressionTransform.verify_as_axiom(src, dst, expr, vt)) is not None:
            return m
        if (m := ExpressionTransform.verify_implies(src, dst, expr, vt)) is not None:
            return m
        if (m := ExpressionTransform.verify_equals(src, dst, expr, vt)) is not None:
            return m
        if (m := ExpressionTransform.verify_context(src, dst, expr, vt)) is not None:
            return m
        return None

    @staticmethod
    def verify_context(
        src: Node, dst: Node, expr: Node, vt: VarTable
    ) -> VarTable | None:
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
                return None
            if src.nodes[1] != dst.nodes[1]:
                return None
            return ExpressionTransform.verify_once(
                src.nodes[0], dst.nodes[0], expr.nodes[1], m
            )
        return None

    @staticmethod
    def verify_as_axiom(
        src: Node, dst: Node, expr: Node, vt: VarTable
    ) -> VarTable | None:
        """
        TRUE >>> axiom
        """
        if src == TRUE and (m := expr.match(dst, vt.copy())) is not None:
            return m
        return None

    @staticmethod
    def verify_implies(
        src: Node, dst: Node, expr: Node, vt: VarTable
    ) -> VarTable | None:
        """
        axiom = (left) >> (right)
        left >>> right
        """
        if isinstance(expr, (Equals, Implies)):
            if (m := expr.nodes[0].match(src, vt.copy())) is not None:
                if expr.nodes[1].match(dst, m) is not None:
                    return m
        return None

    @staticmethod
    def verify_equals(
        src: Node, dst: Node, expr: Node, vt: VarTable
    ) -> VarTable | None:
        """
        axiom = (left) << (right)
        right >>> left
        """
        if isinstance(expr, Equals):
            if (m := expr.nodes[1].match(src, vt.copy())) is not None:
                if expr.nodes[0].match(dst, m) is not None:
                    return m
        return None

    def __eq__(self, other) -> bool:
        if not isinstance(other, ExpressionTransform):
            return False
        return self.expr == other.expr

    def __hash__(self):
        return hash((type(self), self.expr))
