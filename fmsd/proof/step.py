from fmsd.expression import Expression, VarTable
from fmsd.expression.operator import Operator
from fmsd.proof import Proof
from fmsd.rule import Rule


class Step:
    def __init__(self, pos: list[int], rule: Rule, table: VarTable | None = None) -> None:
        self.rule = rule
        self.pos = pos
        self.table = table

    def apply(self, src: Expression) -> Expression:
        src = src.copy()
        if not isinstance(src, Operator) or not self.pos:
            return self.rule(src, self.table)
        target = src.get(self.pos)
        repl = self.rule(target, self.table)
        src.set(self.pos, repl)
        return src


class StepProof(Proof):
    def __init__(self, src: Expression, dst: Expression, steps: list[Step]) -> None:
        Proof.__init__(self, src, dst)
        self.steps = steps

    def verify(self) -> bool:
        exp = self.src
        for step in self.steps:
            exp = step.apply(exp)
        return exp == self.dst
