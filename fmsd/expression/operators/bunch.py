from fmsd.expression.operators import Operator2, Operator1, NumericOperator, BinaryOperator


class Union(Operator2):
    DELIM = ","


class Intersect(Operator2):
    DELIM = "‘"


class In(Operator2, BinaryOperator):
    DELIM = ":"


class Includes(Operator2, BinaryOperator):
    DELIM = "::"


class Count(Operator1, NumericOperator):
    DELIM = "¢"


