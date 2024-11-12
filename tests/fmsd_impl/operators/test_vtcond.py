from fmsd.ast import VarNode
from fmsd_impl.operators import VTCondition


def test_vtcond_replace():
    tree = VTCondition(VarNode("a"), cond=lambda vt: True)
    assert tree.replace([0], VarNode("b")) == VTCondition(
        VarNode("b"), cond=tree.meta["cond"]
    )
