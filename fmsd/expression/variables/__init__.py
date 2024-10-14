from fmsd.expression import Variable, Expression, VarTable
from fmsd.expression.types import Binary, Numeric, Singular


class BinaryVariable(Variable, Binary):
    pass


class NumericVariable(Variable, Numeric):
    pass


class NumericSingularVariable(NumericVariable, Singular):
    def vmatch(self, expr: Expression, matched: VarTable) -> VarTable | None:
        if (matched := NumericVariable.vmatch(self, expr, matched)) is None:
            return None
        if self.singular() != expr.singular():
            return None
        return matched
