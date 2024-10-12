from fmsd.expression import Expression


class BinaryExpression(Expression):
    """
    An expression that evaluates to binary
    """
    pass


class OrderedExpression(Expression):
    pass


class NumericExpression(OrderedExpression):
    """
    An expression that evaluates to number
    """
    pass
