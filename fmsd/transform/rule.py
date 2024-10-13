from fmsd.expression import Expression, VarTable
from fmsd.transform import Transform
from fmsd.rule import Rule, FunctionRule, MatchRule


class RuleTransform(Transform):
    def __init__(self, rule: Rule) -> None:
        Transform.__init__(self)
        self.name = rule.name
        self.rule = rule

    def verify(self, src: Expression, dst: Expression) -> bool:
        if isinstance(self.rule, FunctionRule):
            try:
                return self.rule(src) == dst
            except AssertionError:
                return False
        if isinstance(self.rule, MatchRule):
            if (m := src.match(self.rule.pattern, {})) is not None:
                if dst.match(self.rule.repl, m) == m:
                    return True
            if self.rule.equiv:
                if (m := dst.match(self.rule.pattern, {})) is not None:
                    if src.match(self.rule.repl, m) == m:
                        return True
            return False
        assert False
