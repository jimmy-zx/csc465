from typing import Callable

from fmsd.expression import Expression
from fmsd.expression.constant import Constant


class Operator(Expression):
    def __init__(self, *operands: Expression) -> None:
        self.operands = operands

    def copy(self) -> "Expression":
        return type(self)(*self.operands)

    def eval_var(self, table: dict[str, "Expression"]) -> "Expression":
        return type(self)(*(op.eval_var(table) for op in self.operands))

    def rule_table(self) -> Constant:
        raise NotImplementedError()

    def list_rule(self) -> dict[str, Callable[[], Expression]]:
        return {
            k: getattr(self, k) for k in dir(self) if k.startswith("rule_")
        }

    def is_constant(self) -> bool:
        return all(isinstance(op, Constant) for op in self.operands)

    def __eq__(self, other) -> bool:
        if type(self) != type(other):
            return False
        return self.operands == other.operands