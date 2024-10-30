import fmsd.utils.impl
import fmsd_impl.transforms
import fmsd_impl.transforms.expr
from fmsd.ast import Node
from fmsd.transform import Transform


class Implementation(fmsd.utils.impl.Implementation):
    def node_to_transform(self, node: Node) -> Transform:
        return fmsd_impl.transforms.expr.ExpressionTransform(node)

    def t_all(self) -> dict[str, Transform]:
        return fmsd_impl.transforms.t_all


fmsd.utils.impl.impl = Implementation()
