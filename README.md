# Proof verifier for CSC465:FMSD

[![Pytest](https://github.com/jimmy-zx/csc465/actions/workflows/pytest.yml/badge.svg)](https://github.com/jimmy-zx/csc465/actions/workflows/pytest.yml)

Example: [Solution for 6d](tests/fmsd/proof/test_chain.py) for [Exercise 6](https://www.cs.utoronto.ca/~hehner/aPToP/solutions/Ex6.pdf)

## Roadmap

### Laws

- [ ] Generic
- [x] Binary
- [ ] Numbers
- [ ] Bunches
- [ ] Sets
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

### Recommended exercises

#### L1

- [ ] 0
- [ ] 2

#### L2

- [ ] 14
- [ ] 17

#### L3

- [ ] 6[f](tests/fmsd/proof/test_step.py),[m](tests/fmsd/proof/test_derived_step.py),[p](tests/fmsd/proof/test_derived_step.py),s
- [ ] 7c
- 22

## Structure

### Syntax tree

```
Expression
| Constant - symbols that does not instantiates
| Variable - symbols that can be instantiated
| Operator - symbols that contain one or more operators, and can be evaluated
```

See `fmsd/expression`.

#### Typing

```
BinaryExpression - anything that only evaluates to binary
| BinaryConstant - ⊤ and ⊥ 
| BinaryVariable
| BinaryOperator - ∧∨⇒⇐=⧧ and (if ... then ... else ... fi)
```

See `fmsd/expression/types.py`

### Rule

A rule transforms an expression to an equivalent expression.

See `fmsd/rule`.

### Proof

A proof verifies if two expressions (input and output) are the same, given the hints provided by human.

```
Proof
| StepProof - zero or more steps that applies to the input, single direction (input -> output)
| ChainProof - zero or more proofs that applies to the input, single direction
| EquivProof - a pair of proofs that applies to (input -> output) and (output -> input)
| EquivChainProof - zero or more EquivProof that applies to input and output
```

#### Step

A step is a rule that is applied on a part of expression.

Example: `(a=b)=c` becomes `(b=a)=c` when rule commutative is applied on index `0, 0`.

## Link to course website

[Online course](https://www.cs.utoronto.ca/~hehner/FMSD/)

[Textbook](https://www.cs.utoronto.ca/~hehner/aPToP/)

[CSC465](https://www.cs.toronto.edu/~hehner/465-2104/)
