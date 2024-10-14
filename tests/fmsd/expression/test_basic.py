from fmsd.expression.variables import NumericVariable, NumericSingularVariable


def test_singular():
    assert NumericVariable("a") != NumericSingularVariable("a")
    assert NumericSingularVariable("a") != NumericVariable("a")
