from fmsd.ast import Variable
from fmsd.utils.config import config
import fmsd_impl.patch

assert fmsd_impl.patch


def test_levels():
    for i in range(config.levels * 3):
        print(config.truecolor(i, "hello"))
        print("world")


def test_construction():
    a = Variable("a")
    print(a & a & a & a & a & a & a & a & a & a & a & a & a & a)
