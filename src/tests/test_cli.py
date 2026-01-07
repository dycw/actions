from __future__ import annotations

from pytest import mark, param
from utilities.pathlib import get_repo_root
from utilities.subprocess import run


class TestCLI:
    @mark.parametrize(
        "cmd",
        [
            param("clean-dir"),
            param("conformalize-repo"),
            param("format-requirements"),
            param("publish-package"),
            param("random-sleep"),
            param("replace-sequence-strs"),
            param("run-hooks"),
            param("setup-cronjob"),
            param("tag-commit"),
        ],
    )
    def test_main(self, *, cmd: str) -> None:
        run("action", cmd, cwd=get_repo_root())
