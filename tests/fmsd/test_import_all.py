import glob
import importlib.util
import os
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "file",
    Path("fmsd").rglob("*.py")
)
def test_import_all(file):
    spec = importlib.util.spec_from_file_location("sample", file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)