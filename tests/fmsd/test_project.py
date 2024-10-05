import importlib.util
import re
import subprocess
from pathlib import Path

import pytest


@pytest.mark.parametrize("file", Path("fmsd").rglob("*.py"))
def test_import_all(file):
    spec = importlib.util.spec_from_file_location("sample", file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)


def test_mypy():
    subprocess.run(["mypy", "fmsd", "tests"], check=True)


def test_tree_clean():
    # https://unix.stackexchange.com/questions/155046/determine-if-git-working-directory-is-clean-from-a-script
    p = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, check=True
    )
    assert not p.stdout


def test_readme_intro():
    pattern = re.compile(
        r"\[//]: <> \(MARKER_START__([^\)]*)\)\n.*\[//]: <> \(MARKER_END__([^\)]*)\)",
        flags=re.DOTALL,
    )
    whitelist = {"tests/fmsd/test_intro.py"}
    with open("README.md", "r", encoding="utf-8") as f:
        data = f.read()

    def repl(m: re.Match) -> str:
        assert m.group(1) == m.group(2)
        fname = m.group(1)
        assert fname in whitelist
        hdr = "python" if fname.endswith(".py") else ""
        with open(fname, "r", encoding="utf-8") as fp:
            fdata = fp.read()
        return f"""[//]: <> (MARKER_START__{fname})
```{hdr}
{fdata}
```
[//]: <> (MARKER_END__{fname})"""

    new_data = pattern.sub(repl, data)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_data)
    assert data == new_data


def test_pylint():
    subprocess.run(["pylint", "fmsd", "tests"], check=True)


def test_flake8():
    subprocess.run(["flake8", "fmsd", "tests"], check=True)


def test_black():
    subprocess.run(["black", "fmsd", "tests", "--check"], check=True)
