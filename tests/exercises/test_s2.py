import fmsd_impl.patch.binary
from fmsd.ast.node import VarNode
from fmsd.proof.derived import DerivedChainProof, DerivedEquivChainProof
from fmsd_impl.constants.basic import TRUE
from fmsd_impl.operators.generic import Ternary

assert fmsd_impl.patch.binary


def test_7c():
    """
    Exercise 7c
    """
    b = VarNode("b")
    c = VarNode("c")
    # pylint: disable=invalid-name
    P = VarNode("P")
    Q = VarNode("Q")
    # pylint: enable=invalid-name

    src = Ternary(b, Ternary(c, P, Q), Q)
    dst = Ternary(b & c, P, Q)
    proof = DerivedEquivChainProof(
        src,
        dst,
        [
            Ternary(b, Ternary(c, P, Q), Q),
            (b & Ternary(c, P, Q)) | (~b & Q),
            (b & ((c & P) | (~c & Q))) | (~b & Q),
            ((b & (c & P)) | (b & (~c & Q))) | (~b & Q),
            (b & (c & P)) | ((b & (~c & Q)) | (~b & Q)),
            ((b & c) & P) | (((b & ~c) & Q) | (~b & Q)),
            ((b & c) & P) | ((Q & (b & ~c)) | (Q & ~b)),
            ((b & c) & P) | (Q & ((b & ~c) | ~b)),
            ((b & c) & P) | (((b & ~c) | ~b) & Q),
            ((b & c) & P) | ((~b | (b & ~c)) & Q),
            ((b & c) & P) | (((~b | b) & (~b | ~c)) & Q),
            ((b & c) & P) | (((b | ~b) & (~b | ~c)) & Q),
            ((b & c) & P) | ((TRUE & (~b | ~c)) & Q),
            ((b & c) & P) | ((~b | ~c) & Q),
            ((b & c) & P) | (~(b & c) & Q),
            Ternary(b & c, P, Q),
        ],
    )
    assert proof.verify()
    print(proof.formalize())


def test_22a():
    """
    Exercise 22a
    """
    p = VarNode("p")  # play tennis
    w = VarNode("w")  # watch tennis
    r = VarNode("r")  # read tennis
    stmt1 = (~p) >> w  # If I'm not playing tennis, I'm watching tennis.
    stmt2 = (~w) >> r  # I'm not watching tennis, I'm reading about tennis
    # speaker cannot do more than one of these activities at a time
    stmt3 = ~(p & w)
    stmt4 = ~(w & r)
    stmt5 = ~(p & r)
    for stmt in [stmt1, stmt2, stmt3, stmt4, stmt5]:
        stmt.copy_on_construction = True
    dst = ~p & ~r & w  # the speaker is not reading about tennis
    proof = DerivedChainProof(
        stmt1 & stmt2 & stmt3 & stmt4 & stmt5,
        dst,
        [
            stmt1 & stmt2 & stmt3 & stmt4 & stmt5,
            (stmt1 & stmt2) & stmt3 & stmt4 & stmt5,
            (stmt1 & (~r >> ~~w)) & stmt3 & stmt4 & stmt5,
            (stmt1 & (~r >> w)) & stmt3 & stmt4 & stmt5,
            ((~p | ~r) >> w) & stmt3 & stmt4 & (~p | ~r),
            ((~p | ~r) >> w) & (~p | ~r) & stmt3 & stmt4,
            w & stmt3 & stmt4,
            w & (~p | ~w) & (~w | ~r),
            w & w & w & (~p | ~w) & (~w | ~r),
            ((~p | ~w) & w) & ((~w | ~r) & w) & w,
            ((~w | ~p) & ~~w) & ((~w | ~r) & ~~w) & w,
            (~p) & (~r) & w,
        ],
    )
    assert proof.verify()
