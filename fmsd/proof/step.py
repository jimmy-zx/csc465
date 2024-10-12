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

    def __eq__(self, other) -> bool:
        if not isinstance(other, Step):
            return False
        return self.rule == other.rule and self.pos == other.pos and self.table == other.table


class StepProof(Proof):
    def __init__(self, src: Expression, dst: Expression, steps: list[Step]) -> None:
        Proof.__init__(self, src, dst, str([step.rule.name for step in steps]))
        self.steps = steps

    def verify(self, debug: bool = False) -> bool:
        exp = self.src
        if debug:
            print("    orig:", exp)
        for step in self.steps:
            exp = step.apply(exp)
            if debug:
                print("    step:", exp)
        if debug:
            print("     got:", exp)
            print("expected:", self.dst)
        return exp == self.dst

    def __str__(self) -> str:
        return str(self.dst)

    def __eq__(self, other) -> bool:
        if not isinstance(other, StepProof):
            return False
        return self.src == other.src and self.dst == other.dst and self.steps == other.steps

