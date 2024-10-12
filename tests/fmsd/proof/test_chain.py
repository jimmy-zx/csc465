from fmsd.expression.constants.binary import TRUE
from fmsd.expression.operators.binary import Equals, Implies, Or
from fmsd.expression.variables import BinaryVariable
from fmsd.proof import EquivProof, ChainEquivProof
from fmsd.proof.step import StepProof, Step
from fmsd.rule.rules.binary import rule_associative_equals, rule_commutative_or, rule_inclusion_or, \
    rule_reflexive_equals
from fmsd.rule.rules.generic import rule_symmetry

a = BinaryVariable("a")
b = BinaryVariable("b")
c = BinaryVariable("c")


def test_simple_chain():
    """
    Exercise 6d
    """
    src = Equals(Equals(a, Implies(b, a)), Or(a, b))
    dst = TRUE

    step1 = Equals(Or(a, b), Equals(a, Implies(b, a)))

    step1_fwd = StepProof(
        src,
        step1,
        [Step([0], rule_symmetry), Step([], rule_symmetry), Step([1], rule_symmetry)]
    )
    assert step1_fwd.verify()

    step1_rev = StepProof(
        step1,
        src,
        [Step([1], rule_symmetry), Step([], rule_symmetry), Step([0], rule_symmetry)]
    )
    assert step1_rev.verify()

    step1_eqv = EquivProof(src, step1, step1_fwd, step1_rev)
    assert step1_eqv.verify()

    step2 = Equals(Equals(Or(a, b), a), Implies(b, a))
    step2_eqv = EquivProof(
        step1, step2,
        StepProof(
            step1, step2, [Step([], rule_associative_equals)],
        ),
        StepProof(
            step2, step1, [Step([], rule_associative_equals)],
        )
    )
    assert step2_eqv.verify()

    step3 = Equals(Equals(Or(b, a), a), Implies(b, a))
    step3_eqv = EquivProof(
        step2, step3,
        StepProof(
            step2, step3, [Step([0, 0], rule_commutative_or)],
        ),
        StepProof(
            step3, step2, [Step([0, 0], rule_commutative_or)],
        )
    )
    assert step3_eqv.verify()

    step4 = Equals(Implies(b, a), Implies(b, a))
    step4_eqv = EquivProof(
        step3, step4,
        StepProof(
            step3, step4, [Step([0], rule_inclusion_or)],
        ),
        StepProof(
            step4, step3, [Step([0], rule_inclusion_or)],
        )
    )
    assert step4_eqv.verify()

    step5 = TRUE
    step5_eqv = EquivProof(
        step4, step5,
        StepProof(
            step4, step5, [Step([], rule_reflexive_equals)],
        ),
        StepProof(
            step5, step4, [Step([], rule_reflexive_equals, {"a": Implies(b, a)})],
        )
    )
    assert step5_eqv.verify()

    proof = ChainEquivProof(src, dst, [step1_eqv, step2_eqv, step3_eqv, step4_eqv, step5_eqv])
    assert proof.verify()
    print(proof)  # outputs something like
    """
        ((a=(b⇒a))=(a∨b))       ['symmetry', 'symmetry', 'symmetry']
=       ((a∨b)=(a=(b⇒a)))       ['associative_equals']
=       (((a∨b)=a)=(b⇒a))       ['commutative_or']
=       (((b∨a)=a)=(b⇒a))       ['inclusion_or']
=       ((b⇒a)=(b⇒a))   ['reflexive_equals']
=       ⊤
    """