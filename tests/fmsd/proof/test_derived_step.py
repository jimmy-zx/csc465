from fmsd.expression.variables import BinaryVariable
from fmsd.proof.derived_step import DerivedStepProof
from fmsd.expression.operators.binary import And


a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


def test_simple():
    proof = DerivedStepProof(
        And(a, b), And(b, a)
    )
    assert proof.verify()
    assert proof.hint == "rule_commutative_and"

    proof = DerivedStepProof(
        And(a, b), And(b, c)
    )
    assert not proof.verify()
