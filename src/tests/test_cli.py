from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import mark, param
from utilities.pytest import throttle_test
from utilities.subprocess import run
from utilities.whenever import MINUTE

from actions.clean_dir.constants import CLEAN_DIR_SUB_CMD
from actions.git_clone_with.constants import GIT_CLONE_WITH_SUB_CMD
from actions.pre_commit.conformalize_repo.constants import CONFORMALIZE_REPO_SUB_CMD
from actions.pre_commit.format_requirements.constants import FORMAT_REQUIREMENTS_SUB_CMD
from actions.pre_commit.replace_sequence_strs.constants import (
    REPLACE_SEQUENCE_STRS_SUB_CMD,
)
from actions.pre_commit.touch_empty_py.constants import TOUCH_EMPTY_PY_SUB_CMD
from actions.pre_commit.touch_py_typed.constants import TOUCH_PY_TYPED_SUB_CMD
from actions.pre_commit.update_requirements.constants import UPDATE_REQUIREMENTS_SUB_CMD
from actions.publish_package.constants import PUBLISH_PACKAGE_SUB_CMD
from actions.random_sleep.constants import RANDOM_SLEEP_SUB_CMD
from actions.re_encrypt.constants import RE_ENCRYPT_SUB_CMD
from actions.run_hooks.constants import RUN_HOOKS_SUB_CMD
from actions.setup_cronjob.constants import SETUP_CRONJOB_SUB_CMD
from actions.setup_ssh_config.constants import SETUP_SSH_CONFIG_SUB_CMD
from actions.tag_commit.constants import TAG_COMMIT_SUB_CMD

if TYPE_CHECKING:
    from pathlib import Path


class TestCLI:
    @mark.parametrize(
        "args",
        [
            param(["pre-commit", CONFORMALIZE_REPO_SUB_CMD]),
            param(["pre-commit", FORMAT_REQUIREMENTS_SUB_CMD]),
            param(["pre-commit", REPLACE_SEQUENCE_STRS_SUB_CMD]),
            param(["pre-commit", TOUCH_EMPTY_PY_SUB_CMD]),
            param(["pre-commit", TOUCH_PY_TYPED_SUB_CMD]),
            param(["pre-commit", UPDATE_REQUIREMENTS_SUB_CMD]),
            param([CLEAN_DIR_SUB_CMD]),
            param([PUBLISH_PACKAGE_SUB_CMD]),
            param([RANDOM_SLEEP_SUB_CMD]),
            param([RUN_HOOKS_SUB_CMD]),
            param([SETUP_CRONJOB_SUB_CMD]),
            param([SETUP_SSH_CONFIG_SUB_CMD]),
            param([TAG_COMMIT_SUB_CMD]),
        ],
    )
    @throttle_test(delta=MINUTE)
    def test_main(self, *, args: list[str]) -> None:
        run("action", *args)

    @mark.parametrize("cmd", [param(GIT_CLONE_WITH_SUB_CMD), param(RE_ENCRYPT_SUB_CMD)])
    @throttle_test(delta=MINUTE)
    def test_requires_file(self, *, cmd: str, tmp_path: Path) -> None:
        file = tmp_path / "file.txt"
        file.touch()
        run("action", cmd, str(file), "owner", "repo", cwd=tmp_path)
