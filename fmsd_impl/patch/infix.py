# from fmsd.expression.operators.numeric import Max, Min
from fmsd.ast.node import Node
from fmsd.utils.infix import InfixOperator
from fmsd_impl.operators.generic import Equals, NotEquals

# pylint: disable=invalid-name


# noinspection PyPep8Naming
@InfixOperator[Node, Node, Node]
def EQ(lhs, rhs):
    return Equals(lhs, rhs)


# noinspection PyPep8Naming
@InfixOperator[Node, Node, Node]
def NEQ(lhs, rhs):
    return NotEquals(lhs, rhs)


# @InfixOperator[Node, Node, Node]
# def MAX(lhs, rhs):
#     return Max(lhs, rhs)
#
#
# @InfixOperator[Node, Node, Node]
# def MIN(lhs, rhs):
#     return Min(lhs, rhs)


__all__ = [
    "EQ",
    "NEQ",
]
