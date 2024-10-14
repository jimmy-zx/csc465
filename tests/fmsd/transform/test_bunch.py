from fmsd.expression.variables import NumericSingularVariable
from fmsd.expression.operators.bunch import In, Union
from fmsd.expression.constants.numeric import ZERO
from fmsd.expression.constants.bunch import NAT
from fmsd.expression.constants.binary import TRUE
# noinspection PyUnresolvedReferences
import fmsd.utils.patch.binary
# noinspection PyUnresolvedReferences
import fmsd.utils.patch.numeric
from fmsd.transform.expr import ExpressionTransform
from fmsd.transform.transforms.axioms.bunch import axiom_generalization


def test_generalization():
    n = NumericSingularVariable("n")
    src = TRUE
    dst = In(n * ZERO, Union(n * ZERO, n * NAT))
    assert ExpressionTransform(axiom_generalization, "").verify(src, dst)