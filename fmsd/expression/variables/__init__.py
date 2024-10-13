from fmsd.expression.types import Binary, Numeric
from fmsd.expression import Variable


class BinaryVariable(Variable, Binary):
    pass


class NumericVariable(Variable, Numeric):
    pass