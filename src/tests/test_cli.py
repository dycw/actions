from __future__ import annotations

from pytest import mark, param
from utilities.pathlib import get_repo_root
from utilities.pytest import throttle
from utilities.subprocess import run
from utilities.whenever import MINUTE

from actions.pre_commit.conformalize_repo.constants import CONFORMALIZE_REPO_SUB_CMD
from actions.pre_commit.format_requirements.constants import FORMAT_REQUIREMENTS_SUB_CMD
from actions.pre_commit.replace_sequence_strs.constants import (
    REPLACE_SEQUENCE_STRS_SUB_CMD,
)
from actions.pre_commit.touch_empty_py.constants import TOUCH_EMPTY_PY_SUB_CMD


class TestCLI:
    @mark.parametrize(
        "args",
        [
            param(["clean-dir"]),
            param(["pre-commit", CONFORMALIZE_REPO_SUB_CMD]),
            param(["pre-commit", FORMAT_REQUIREMENTS_SUB_CMD]),
            param(["pre-commit", REPLACE_SEQUENCE_STRS_SUB_CMD]),
            param(["pre-commit", TOUCH_EMPTY_PY_SUB_CMD]),
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
