import importlib.util
import subprocess
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


def test_mypy():
    subprocess.run(["mypy", "fmsd", "tests"], check=True)


def test_tree_clean():
    # https://unix.stackexchange.com/questions/155046/determine-if-git-working-directory-is-clean-from-a-script
    p = subprocess.run(["git", "status", "--porcelain"], capture_output=True, check=True)
    assert not p.stdout


def test_pylint():
    subprocess.run(
        ["pylint", "fmsd", "tests"],
        check=True
    )


def test_flake8():
    subprocess.run(
        ["flake8", "fmsd", "tests"],
        check=True
    )
