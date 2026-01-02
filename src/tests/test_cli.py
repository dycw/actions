from __future__ import annotations

from pytest import mark, param
from utilities.pathlib import get_repo_root
from utilities.subprocess import run


class TestCLI:
    @mark.parametrize(
        "cmd",
        [
            param("hooks"),
            param("publish"),
            param("requirements"),
            param("sequence-strs"),
            param("sleep"),
            param("tag"),
        ],
    )
    def test_main(self, *, cmd: str) -> None:
        run("action", cmd, cwd=get_repo_root())
