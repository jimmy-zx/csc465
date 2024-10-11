from fmsd.expression import Expression
from fmsd.proof import Proof
from fmsd.rule import MatchRule, FunctionRule, Rule
from fmsd.rule.rules import ruleset as global_ruleset


class DerivedStepProof(Proof):
    def __init__(self, src: Expression, dst: Expression) -> None:
        Proof.__init__(self, src, dst, "")

    def verify(self, debug: bool = False) -> bool:
        idx = self.src.diff(self.dst)
        src = self.src.get(idx)
        dst = self.dst.get(idx)
        if (hint := self.verify_ruleset(src, dst, global_ruleset)) is None:
            return False
        self.hint = hint
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
