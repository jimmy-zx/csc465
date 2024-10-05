from fmsd.expression import Expression
from fmsd.expression.constant import Constant
from fmsd.expression.constants import TRUE, FALSE
from fmsd.expression.operators import BinaryOperator, BinaryOperator2WithBinaryOperands
from fmsd.expression.types import BinaryExpression


class Flip(BinaryOperator):
    def __init__(self, operand: Expression) -> None:
        BinaryOperator.__init__(self, operand)
        assert isinstance(operand, BinaryExpression)
        self.op = operand

    def __str__(self) -> str:
        return f"¬(" + str(self.op) + ")"

    def rule_table(self) -> Constant:
        assert self.is_constant()
        if self.op == TRUE:
            return FALSE
        return TRUE

    def rule_unequality(self) -> Expression:
        assert isinstance(self.op, Equals)
        return NotEquals(*self.op.operands).copy()

    def rule_double_negation(self) -> Expression:
        assert isinstance(self.op, Flip)
        return self.op.op.copy()

    def rule_duality(self) -> Expression:
        if isinstance(self.op, And):
            return Or(Flip(self.op.lhs), Flip(self.op.rhs)).copy()
        if isinstance(self.op, Or):
            return And(Flip(self.op.lhs), Flip(self.op.rhs)).copy()
        assert False


class And(BinaryOperator2WithBinaryOperands):
    def rule_table(self) -> Constant:
        assert self.is_constant()
        if self.operands[0] == TRUE and self.operands[1] == TRUE:
            return TRUE
        return FALSE

    def __str__(self) -> str:
        return "({})∧({})".format(str(self.lhs), str(self.rhs))

    def rule_transitivity(self) -> Expression:
        assert isinstance(self.lhs, Equals)
        assert isinstance(self.rhs, Equals)
        assert self.lhs.operands[1] == self.rhs.operands[0]
        return Equals(self.lhs.operands[0], self.rhs.operands[1]).copy()

    def rule_noncontradiction(self) -> Expression:
        assert isinstance(self.rhs, Flip)
        assert self.lhs == self.rhs.operands[0]
        return FALSE

    def rule_base(self) -> Expression:
        if self.rhs == FALSE:
            return FALSE
        assert False

    def rule_duality(self) -> Expression:
        pass


class Or(BinaryOperator2WithBinaryOperands):
    def rule_table(self) -> Constant:
        assert self.is_constant()
        if self.operands[0] == TRUE or self.operands[1] == TRUE:
            return TRUE
        return FALSE

    def __str__(self) -> str:
        return "({})∨({})".format(str(self.lhs), str(self.rhs))

    def rule_excluded_middle(self) -> Expression:
        assert isinstance(self.rhs, Flip)
        assert self.lhs == self.rhs.operands[0]
        return TRUE

    def rule_base(self) -> Expression:
        if self.rhs == TRUE:
            return TRUE
        assert False


class Implies(BinaryOperator2WithBinaryOperands):
    def __str__(self) -> str:
        return "({})⇒({})".format(str(self.lhs), str(self.rhs))

    def rule_table(self) -> Constant:
        assert self.is_constant()
        if self.operands[0] == FALSE or self.operands[1] == TRUE:
            return TRUE
        return FALSE

    def rule_base(self) -> Expression:
        if self.rhs == TRUE:
            return TRUE
        if self.lhs == FALSE:
            return TRUE
        assert False

    def rule_mirror(self) -> Expression:
        return ImpliedBy(self.rhs, self.lhs).copy()


class ImpliedBy(BinaryOperator2WithBinaryOperands):
    def __str__(self) -> str:
        return "({})⇐({})".format(str(self.lhs), str(self.rhs))

    def rule_table(self) -> Constant:
        assert self.is_constant()
        if self.operands[0] == TRUE or self.operands[1] == FALSE:
            return TRUE
        return FALSE

    def rule_mirror(self) -> Expression:
        return Implies(self.rhs, self.lhs).copy()


class Equals(BinaryOperator2WithBinaryOperands):
    def __str__(self) -> str:
        return "({})=({})".format(str(self.lhs), str(self.rhs))

    def rule_table(self) -> Constant:
        assert self.is_constant()
        if self.operands[0] == self.operands[1]:
            return TRUE
        return FALSE

    def rule_reflexivity(self) -> Expression:
        assert self.operands[0] == self.operands[1]
        return TRUE

    def rule_symmetry(self) -> Expression:
        return Equals(*self.operands[::-1]).copy()


class NotEquals(BinaryOperator2WithBinaryOperands):
    def __str__(self) -> str:
        return "({})⧧({})".format(str(self.lhs), str(self.rhs))

    def rule_table(self) -> Constant:
        assert self.is_constant()
        if self.operands[0] != self.operands[1]:
            return TRUE
        return FALSE

    def rule_unequality(self) -> Expression:
        return Flip(Equals(self.lhs, self.rhs)).copy()


class Ternary(BinaryOperator):
    def __init__(self, if_: Expression, then: Expression, else_: Expression) -> None:
        BinaryOperator.__init__(self, if_, then, else_)
        assert isinstance(if_, BinaryExpression)
        assert isinstance(then, BinaryExpression)
        assert isinstance(else_, BinaryExpression)

    def __str__(self) -> str:
        return "if {} then {} else {} fi".format(*map(str, self.operands))

    def rule_table(self) -> Constant:
        assert self.is_constant()
        if self.operands[0] == TRUE:
            if self.operands[1] == TRUE:
                return TRUE
            return FALSE
        if self.operands[2] == TRUE:
            return TRUE
        return FALSE

    def rule_case_base(self) -> Expression:
        assert isinstance(self.operands[0], Constant)
        if self.operands[0] == TRUE:
            return self.operands[1].copy()
        return self.operands[2].copy()

    def rule_case_idempotent(self) -> Expression:
        assert self.operands[1] == self.operands[2]
        return self.operands[1]

    def rule_case_reversal(self) -> Expression:
        return Ternary(Flip(self.operands[0]), self.operands[2], self.operands[1])
