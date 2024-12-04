import re
import subprocess

import pytest

TARGET_FILES = ["fmsd", "fmsd_impl", "tests", "setup.py", "build_isolated.py"]


@pytest.mark.order(-1)
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


def test_mypy():
    subprocess.run(["mypy"] + TARGET_FILES, check=True)


@pytest.mark.order(-1)
def test_pylint():
    subprocess.run(["pylint", "-j", "0"] + TARGET_FILES, check=True)


def test_flake8():
    subprocess.run(["flake8"] + TARGET_FILES, check=True)


def test_black():
    subprocess.run(["black", "--check"] + TARGET_FILES, check=True)


def test_import_linter():
    subprocess.run(["lint-imports"], check=True)


def test_isort():
    p = subprocess.run(
        ["isort", "fmsd", "fmsd_impl", "tests", "--diff"],
        check=True,
        capture_output=True,
    )
    status = p.stdout == b""
    assert status


@pytest.mark.order(-1)
def test_build():
    subprocess.run(["make", "build"], check=True)
