import itertools

from fmsd.expression import Expression, VarTable
from fmsd.proof import Proof, ChainProof, EquivProof
from fmsd.proof.step import StepProof, Step
from fmsd.rule import MatchRule, FunctionRule, Rule
from fmsd.rule.rules import ruleset as global_ruleset


class DerivedStepProof(Proof):
    def __init__(self, src: Expression, dst: Expression) -> None:
        Proof.__init__(self, src, dst, "")
        self.derived_proof: Proof | None = None

    def verify(self, debug: bool = False) -> bool:
        idx = self.src.diff(self.dst)
        if idx is None:
            return True
        steps = []
        src = self.src
        while src != self.dst:
            if (res := self.refine_once(src, self.dst, global_ruleset)) is None:
                raise Exception(f"Failed to find a rule for ({self.src}) {src} to {self.dst}")
            rule, idx, table, src = res
            steps.append(Step(idx, rule, table))
        self.derived_proof = StepProof(
            self.src, self.dst, steps
        )
        try:
            assert self.derived_proof.verify()
        except Exception as ex:
            raise Exception("Failed to verify derived proof") from ex
        self.hint = self.derived_proof.hint
        return True

    def formalize(self) -> "Proof":
        if not self.derived_proof:
            assert self.verify()
        assert self.derived_proof is not None
        return self.derived_proof

    def __eq__(self, other) -> bool:
        return self.src == other.src and self.dst == other.dst

    @staticmethod
    def refine_once(src: Expression, dst: Expression, ruleset: dict[str, Rule]) -> tuple[Rule, list[
        int], VarTable, Expression] | None:
        assert src.diff(dst) is not None
        for i in itertools.count(start=0):
            idx = src.diff(dst, start=i)
            if idx is None:
                return None
            if (res := DerivedStepProof.verify_ruleset(src.get(idx), dst.get(idx), ruleset)) is not None:
                if not idx:
                    refined = dst
                else:
                    refined = src.copy()
                    refined.set(idx, dst.get(idx))

                return res[0], idx, res[1], refined
        assert False

    @staticmethod
    def verify_ruleset(src: Expression, dst: Expression, ruleset: dict[str, Rule]) -> tuple[Rule, VarTable] | None:
        for _, rule in ruleset.items():
            if (table := DerivedStepProof.verify_once(src, dst, rule)) is not None:
                return rule, table
        return None

    @staticmethod
    def verify_once(src: Expression, dst: Expression, rule: Rule) -> VarTable | None:
        if isinstance(rule, MatchRule):
            if (m := src.match(rule.pattern, {})) is not None:
                if dst.match(rule.repl, m) == m:
                    return m
            if rule.equiv:
                if (m := dst.match(rule.pattern, {})) is not None:
                    if src.match(rule.repl, m) == m:
                        return m
            return None
        if isinstance(rule, FunctionRule):
            try:
                if dst == rule(src):
                    return VarTable()
            except AssertionError:
                return None
        assert None


class DerivedChainProof(ChainProof):
    def __init__(self, src: Expression, dst: Expression, steps: list[Expression]) -> None:
        ChainProof.__init__(self, src, dst, [
            DerivedStepProof(steps[i], steps[i + 1])
            for i in range(len(steps) - 1)
        ])


class DerivedEquivChainProof(EquivProof):
    def __init__(self, src: Expression, dst: Expression, steps: list[Expression]) -> None:
        EquivProof.__init__(
            self,
            src, dst,
            DerivedChainProof(src, dst, steps),
            DerivedChainProof(dst, src, steps[::-1])
        )
