from fmsd.ast_ext import Constant
from fmsd_impl.constants import ONE, ZERO
from fmsd_impl.operators import Join, List, ListAt
from fmsd_impl.transforms.constant.clist import t_at


def test_at():
    assert t_at.verify(
        ListAt(
            List(
                Join.bin_list(
                    List(Join(Constant("2"), Constant("3"))),
                    Constant("4"),
                    List(
                        Join(
                            Constant("5"),
                            List(Join(Constant("6"), Constant("7"))),
                        )
                    ),
                )
            ),
            Join.bin_list(Constant("2"), ONE, ZERO),
        ),
        Constant("6"),
    )
