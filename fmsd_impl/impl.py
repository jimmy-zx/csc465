import fmsd.utils.impl
import fmsd_impl.transforms
import fmsd_impl.transforms.expr
from fmsd.ast import Node
from fmsd.transform import Transform, TransformManager
from fmsd.transform.manager import ListTransformManager
from fmsd_impl.transforms import t_all


class Implementation(fmsd.utils.impl.Implementation):
    def __init__(self) -> None:
        self.manager = ListTransformManager(t_all)

    def node_to_transform(self, node: Node) -> Transform:
        return fmsd_impl.transforms.expr.ExpressionTransform(node)

    def transform_manager(self) -> TransformManager:
        return self.manager


fmsd.utils.impl.impl = Implementation()
