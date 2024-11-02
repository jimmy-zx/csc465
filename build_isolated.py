#!/usr/bin/env python3

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

        subprocess.run(cwd / "build.sh", cwd=tmpdir, check=True)


if __name__ == "__main__":
    main()
