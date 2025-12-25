from __future__ import annotations

from subprocess import check_call

from pytest import mark, param
from utilities.pathlib import get_repo_root


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
        _ = check_call(["action", cmd], cwd=get_repo_root())
