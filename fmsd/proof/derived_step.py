from fmsd.expression import Expression
from fmsd.proof import Proof, ChainProof
from fmsd.proof.step import StepProof, Step
from fmsd.rule import MatchRule, FunctionRule, Rule
from fmsd.rule.rules import ruleset as global_ruleset


class DerivedStepProof(Proof):
    def __init__(self, src: Expression, dst: Expression) -> None:
        Proof.__init__(self, src, dst, "")
        self.derived_proof: Proof | None = None

    def verify(self, debug: bool = False) -> bool:
        idx = self.src.diff(self.dst)
        src = self.src.get(idx)
        dst = self.dst.get(idx)
        if (rule := self.verify_ruleset(src, dst, global_ruleset)) is None:
            return False
        self.hint = rule.name
        self.derived_proof = StepProof(
            self.src, self.dst, [
                Step(idx, rule)
            ]
        )
        assert self.derived_proof.verify(debug=debug)
        return True

    def formalize(self) -> "Proof":
        if not self.derived_proof:
            assert self.verify()
        return self.derived_proof

    def __eq__(self, other) -> bool:
        return self.src == other.src and self.dst == other.dst

    @staticmethod
    def verify_ruleset(src: Expression, dst: Expression, ruleset: dict[str, Rule], debug: bool = False) -> Rule | None:
        for _, rule in ruleset.items():
            if DerivedStepProof.verify_once(src, dst, rule, debug):
                return rule
        return None

    @staticmethod
    def verify_once(src: Expression, dst: Expression, rule: Rule, debug: bool = False) -> bool:
        if isinstance(rule, MatchRule):
            if (m := src.match(rule.pattern, {})) is not None:
                if dst.match(rule.repl, m) == m:
                    return True
            if rule.equiv:
                if (m := dst.match(rule.pattern, {})) is not None:
                    if src.match(rule.repl, m) == m:
                        return True
            return False
        if isinstance(rule, FunctionRule):
            try:
                if dst == rule(src):
                    return True
            except AssertionError:
                return False
        assert False


class DerivedChainProof(ChainProof):
    def __init__(self, src: Expression, dst: Expression, steps: list[Expression]) -> None:
        ChainProof.__init__(self, src, dst, [
            DerivedStepProof(steps[i], steps[i + 1])
            for i in range(len(steps) - 1)
        ])
