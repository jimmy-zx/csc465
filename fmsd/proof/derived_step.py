from fmsd.expression import Expression
from fmsd.proof import Proof
from fmsd.rule import MatchRule, FunctionRule, Rule
from fmsd.rule.rules import ruleset as global_ruleset


class DerivedStepProof(Proof):
    def __init__(self, src: Expression, dst: Expression) -> None:
        Proof.__init__(self, src, dst, "")

    def verify(self, debug: bool = False) -> bool:
        diffs = self.src.diff_all(self.dst)
        hints = []
        for diff in diffs:
            src = self.src.get(diff)
            dst = self.dst.get(diff)
            if (hint := self.verify_ruleset(src, dst, global_ruleset)) is None:
                return False
            hints.append(hint)
        self.hint = " ".join(hints)
        return True

    @staticmethod
    def verify_ruleset(src: Expression, dst: Expression, ruleset: dict[str, Rule], debug: bool = False) -> str | None:
        for name, rule in ruleset.items():
            if DerivedStepProof.verify_once(src, dst, rule, debug):
                return name
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
