from fmsd.expression.operators.binary import Implies
from fmsd.expression.operators.generic import Equals


def MatchRule(src, dst, equiv: bool = True):  # pylint: disable=invalid-name
    assert equiv
    if equiv:
        return Equals(src, dst)
    return Implies(src, dst)
