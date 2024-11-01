# type: ignore

import os
import subprocess
from datetime import datetime

from setuptools import setup


def get_version():
    version = "0.1.0"

    repo_file = "FMSDREPO"
    version_file = "VERSION"

    if not os.path.isfile(repo_file) and os.path.isfile(version_file):
        with open(version_file, "r", encoding="ascii") as f:
            return f.read()

    def get_git_root() -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return (
            subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], cwd=dir_path
            )
            .decode("ascii")
            .strip()
        )

    cwd = get_git_root()

    def get_git_commit_hash() -> str:
        # https://stackoverflow.com/questions/949314
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=cwd)
            .decode("ascii")
            .strip()
        )

    def check_git_dirty() -> bool:
        return subprocess.check_output(["git", "status", "--porcelain"], cwd=cwd) != b""

    fq_version = version + "+" + get_git_commit_hash()
    if check_git_dirty():
        fq_version += ".dirty"
        fq_version += datetime.now().strftime("%Y%m%d%H%M%S%f")

    with open(version_file, "w", encoding="ascii") as f:
        f.write(fq_version)

    return fq_version


setup(version=get_version())
