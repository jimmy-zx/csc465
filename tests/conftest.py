import pytest

import fmsd.utils.impl
import fmsd_impl.impl

assert fmsd_impl.impl


@pytest.fixture(autouse=True)
def clear_cache():
    assert fmsd.utils.impl.impl is not None
    fmsd.utils.impl.impl.transform_manager().reset()
    yield
