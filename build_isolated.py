#!/usr/bin/env python3

"""
Tests the project in an isolated environment.

This script should NEVER be called by pytest.
"""

import os
import pathlib
import shutil
import subprocess
import tempfile


def get_git_root() -> str:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return (
        subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=dir_path)
        .decode("ascii")
        .strip()
    )


def main():
    with tempfile.TemporaryDirectory() as tmpdir_name:
        tmpdir = pathlib.Path(tmpdir_name)
        cwd = pathlib.Path(get_git_root())

        files = (
            subprocess.check_output(["git", "ls-files"], cwd=cwd)
            .decode("ascii")
            .split()
        )

        dirs = set()
        for file in files:
            if (dirname := os.path.dirname(file)) not in dirs:
                pathlib.Path(tmpdir / dirname).mkdir(parents=True, exist_ok=True)
                dirs.add(dirname)
            shutil.copy2(cwd / file, tmpdir / file)

        build_script = """
#!/usr/bin/env bash

set -e

USAGE="Usage: python3 build_isolated.py"

if [ -d venv ]; then
  echo "$USAGE"
  exit 1
fi

if [ -d .git ]; then
  echo "$USAGE"
  exit 1
fi

git init
git add .
git commit -m "foreign build dummy commit"

python3 -m venv venv
source venv/bin/activate
make install
make test
        """

        with open(tmpdir / "build.sh", "w", encoding="ascii") as fp:
            fp.write(build_script)

        subprocess.run(["bash", tmpdir / "build.sh"], cwd=tmpdir, check=True)


if __name__ == "__main__":
    main()
