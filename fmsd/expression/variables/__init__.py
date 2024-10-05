from fmsd.expression import Variable, Expression, VarTable
from fmsd.expression.types import Binary, Numeric, Singular, Type


class AnyVariable(Variable):
    def type(self) -> Type:
        return Type.ANY


class BinaryVariable(Variable, Binary):
    pass


class NumericVariable(Variable, Numeric):
    pass


class NumericSingularVariable(NumericVariable, Singular):
    def vmatch(self, expr: Expression, matched: VarTable) -> VarTable | None:
        if (res := NumericVariable.vmatch(self, expr, matched)) is None:
            return None
        if self.singular() != expr.singular():
            return None
        return res


class SetVariable(Variable):
    def __init__(self, name: str, content_type: Type) -> None:
        Variable.__init__(self, name)
        self._content_type = content_type

    def type(self) -> Type:
        return Type.SET

    def content_type(self) -> Type:
        return self._content_type

    def vmatch(self, expr: Expression, matched: VarTable) -> VarTable | None:
        if (res := NumericVariable.vmatch(self, expr, matched)) is None:
            return None
        if not self.content_type().match(expr.content_type()):
            return None
        return res
