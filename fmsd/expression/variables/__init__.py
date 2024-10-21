from fmsd.expression import Variable, Expression, VarTable
from fmsd.expression.types import Binary, Numeric, Singular, Type


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
    def __init__(self, name: str, set_type: Type) -> None:
        Variable.__init__(self, name)
        self._set_type = set_type

    def type(self) -> Type:
        return Type.SET

    def set_type(self) -> Type:
        return self._set_type
