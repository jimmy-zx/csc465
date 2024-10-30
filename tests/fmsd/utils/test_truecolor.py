from fmsd.ast import Variable
from fmsd.utils.config import config
import fmsd_impl.patch

assert fmsd_impl.patch


def test_levels():
    for i in range(config.levels * 6):
        print(config.truecolor(i, "h"), end="")
        print("l", end="")


def test_construction():
    a = Variable("a")
    print(a & a & a & a & a & a & a & a & a & a & a & a & a & a)
