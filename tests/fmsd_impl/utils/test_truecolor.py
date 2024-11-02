import fmsd_impl.patch
from fmsd.ast import Variable
from fmsd.utils.config import config

assert fmsd_impl.patch


def test_levels():
    for i in range(config.levels * 6):
        print(config.truecolor(i, "h"), end="")
        print("l", end="")
    for i in range(10):
        assert config.truecolor(config.max_level + i, "h") == "h"


def test_construction():
    a = Variable("a")
    print(a & a & a & a & a & a & a & a & a & a & a & a & a & a)
