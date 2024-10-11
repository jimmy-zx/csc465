from fmsd.expression.variables import BinaryVariable
from fmsd.proof.derived_step import DerivedStepProof
from fmsd.expression.operators.binary import And


a = BinaryVariable("a")
b = BinaryVariable("b")


def test_simple():
    proof = DerivedStepProof(
        And(a, b), And(b, a)
    )
    # assert proof.verify(debug=True)
    # assert proof.hint == "rule_commutative_and"
