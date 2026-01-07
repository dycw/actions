from __future__ import annotations

from pytest import mark, param
from utilities.pathlib import get_repo_root
from utilities.pytest import throttle
from utilities.subprocess import run
from utilities.whenever import MINUTE


class TestCLI:
    @mark.parametrize(
        "args",
        [
            param(["clean-dir"]),
            param(["pre-commit", "conformalize-repo"]),
            param(["pre-commit", "format-requirements"]),
            param(["pre-commit", "replace-sequence-strs"]),
            param(["publish-package"]),
            param(["random-sleep"]),
            param(["run-hooks"]),
            param(["setup-cronjob"]),
            param(["tag-commit"]),
        ],
    )
    @throttle(delta=MINUTE)
    def test_main(self, *, args: list[str]) -> None:
        run("action", *args, cwd=get_repo_root())
