import fmsd.utils.impl
from fmsd.transform import TransformManager
from fmsd.transform.manager import ListTransformManager
from fmsd_impl.transforms import t_all


class Implementation(fmsd.utils.impl.Implementation):
    def __init__(self) -> None:
        self.manager = ListTransformManager(t_all)

    def transform_manager(self) -> TransformManager:
        return self.manager


fmsd.utils.impl.impl = Implementation()
