import fmsd.utils.patch.binary
from fmsd.expression.constants.binary import FALSE
from fmsd.expression.operators.binary import Or
from fmsd.expression.operators.generic import Equals, NotEquals
from fmsd.expression.variables import BinaryVariable
from fmsd.proof import ChainProof
from fmsd.proof.derived_step import DerivedStepProof, TransformProof
from fmsd.transform.expr import ExpressionTransform
from fmsd.transform.transforms.axioms.binary import (
    axiom_base_and,
)
from fmsd.transform.transforms.prop import t_associative
from fmsd.utils.patchops.infix import EQ, NEQ

assert fmsd.utils.patch.binary


def test_intro():
    # declare a variable
    x = BinaryVariable("x")
    y = BinaryVariable("y")
    z = BinaryVariable("z")

    # build AST directly
    Or(x, y)

    # or use infix operators
    x | y  # pylint: disable=W0104

    assert Or(x, y) == x | y

    # operators == and != are used for comparing equality of the ASTs
    # use Equals or @ EQ @ to construct the "equals" operator

    assert Equals(x, y) == x @ EQ @ y
    assert NotEquals(x, y) == x @ NEQ @ y

    # we have a library of axioms, for example ⊥∧x=⊥ (axiom_base_and)
    assert ExpressionTransform(axiom_base_and).verify(x & FALSE, FALSE)

    # we can write a proof using this axiom
    proof1 = TransformProof(
        src=x & FALSE,
        dst=FALSE,
        transform=ExpressionTransform(axiom_base_and),
        index=[],
    )
    assert proof1.verify()

    # or we can automatically detect the axiom to use
    proof2 = DerivedStepProof(src=x & FALSE, dst=FALSE)
    assert proof2.verify()

    # the formalized proof uses the same proof as our previous proof,
    # except this is a ChainProof with length 1
    assert proof2.formalize() == ChainProof(src=x & FALSE, dst=FALSE, proofs=[proof1])

    # we can do something complex with associative operators in one step
    assert DerivedStepProof(src=((x & y) & (y & z)), dst=(x & (y & (y & z)))).verify()

    # we can also use multiple transformations in parallel
    # note: rule `t_associative` also works on operators that are commutative and assocative
    proof3 = DerivedStepProof(src=(x & y) | (y & z), dst=(y & x) | (z & y))
    assert proof3.verify()
    assert proof3.formalize() == ChainProof(
        src=(x & y) | (y & z),
        dst=(y & x) | (z & y),
        proofs=[
            TransformProof((x & y) | (y & z), (y & x) | (y & z), t_associative, [0]),
            TransformProof((y & x) | (y & z), (y & x) | (z & y), t_associative, [1]),
        ],
    )

    # for more complex proofs, see `tests/exercises`
