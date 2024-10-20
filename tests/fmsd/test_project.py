import importlib.util
from pathlib import Path
import subprocess

import pytest


@pytest.mark.parametrize(
    "file",
    Path("fmsd").rglob("*.py")
)
def test_import_all(file):
    spec = importlib.util.spec_from_file_location("sample", file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)


def test_mypy():
    subprocess.run(["mypy", "fmsd", "--check-untyped-defs"], check=True)


def test_tree_clean():
    # https://unix.stackexchange.com/questions/155046/determine-if-git-working-directory-is-clean-from-a-script
    p = subprocess.run(["git", "status", "--porcelain"], capture_output=True)
    assert not p.stdout