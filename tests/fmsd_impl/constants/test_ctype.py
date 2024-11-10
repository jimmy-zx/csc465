from fmsd.ast_ext import Constant
from fmsd_impl.constants import ONE, ZERO
from fmsd_impl.operators import Join, List
from fmsd_impl.transforms.ctype import to_list


def test_to_list():
    node = List(
        Join.bin_list(
            ZERO,
            List(
                Join.bin_list(
                    ONE,
                    Constant("2"),
                    List(
                        Join.bin_list(
                            Constant("3"),
                            Constant("4"),
                        )
                    ),
                )
            ),
            Constant("5"),
        )
    )
    assert to_list(node) == [
        ZERO,
        [ONE, Constant("2"), [Constant("3"), Constant("4")]],
        Constant("5"),
    ]
