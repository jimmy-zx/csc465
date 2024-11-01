# Proof verifier for CSC465:FMSD

[![Pytest](https://github.com/jimmy-zx/csc465/actions/workflows/pytest.yml/badge.svg)](https://github.com/jimmy-zx/csc465/actions/workflows/pytest.yml)

## Introduction

[//]: <> (MARKER_START__tests/fmsd/test_intro.py)
```python
import fmsd_impl.patch.binary
from fmsd.ast.node import Variable
from fmsd.proof.chain import ChainProof
from fmsd.proof.derived import DerivedStepProof
from fmsd.proof.transform import TransformProof
from fmsd_impl.constants.basic import FALSE
from fmsd_impl.operators.binary import Or
from fmsd_impl.operators.generic import Equals, NotEquals
from fmsd_impl.patch.infix import EQ, NEQ
from fmsd_impl.transforms.axioms.binary import axiom_base_and
from fmsd_impl.transforms.expr import ExpressionTransform
from fmsd_impl.transforms.prop import t_associative

assert fmsd_impl.patch.binary


def test_intro():
    # declare a variable
    x = Variable("x")
    y = Variable("y")
    z = Variable("z")

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

```
[//]: <> (MARKER_END__tests/fmsd/test_intro.py)

## Roadmap

### Laws

- [x] Generic
- [x] Binary
- [x] Numbers
- [x] Bunches
- [x] Sets
- [ ] Strings
- [ ] Lists
- [ ] Functions
- [ ] Quantifiers
- [ ] Limits
- [ ] Specifications and programs
- [ ] Substitution
- [ ] Assertions
- [ ] Refinement
- [ ] Names
- [ ] Distribution

## Architecture

- core `fmsd`

```
| ast: basic building unit
| | Node: a tree node of arbitrary (0+) children
| | Variable: a named leaf node that indicates it should be replaced
| ast_ext: extension to ast
| | Constant: a named leaf node
| | Operator: helper for creating operators (node with fixed number of children)
| transform: verifies equivalency
| | Transform: interface to specify src node can be converted to dst node
| proof: complex transforms
| | Proof: interface for a complex transform (src => dst)
| | TransformProof: wrapper for proofs with a single transform
| | DerivedStepProof: automatically find transforms given src and dst
```


## Link to course website

[Online course](https://www.cs.utoronto.ca/~hehner/FMSD/)

[Textbook](https://www.cs.utoronto.ca/~hehner/aPToP/)

[CSC465](https://www.cs.toronto.edu/~hehner/465-2104/)
