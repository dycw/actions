from __future__ import annotations

from typing import TYPE_CHECKING

from click.testing import CliRunner
from pytest import mark, param
from utilities.constants import MINUTE, TEMP_DIR
from utilities.pytest import skipif_ci, throttle_test
from utilities.subprocess import run

import actions.clean_dir.cli
import actions.cli
import actions.publish_package.cli
import actions.random_sleep.cli
import actions.re_encrypt.cli
import actions.register_gitea_runner.cli
import actions.set_up_cron.cli
import actions.tag_commit.cli
from actions.clean_dir.cli import CLEAN_DIR_SUB_CMD
from actions.publish_package.cli import PUBLISH_PACKAGE_SUB_CMD
from actions.random_sleep.cli import RANDOM_SLEEP_SUB_CMD
from actions.re_encrypt.cli import RE_ENCRYPT_SUB_CMD
from actions.register_gitea_runner.constants import REGISTER_GITEA_RUNNER_SUB_CMD
from actions.set_up_cron.cli import SET_UP_CRON_SUB_CMD
from actions.tag_commit.cli import TAG_COMMIT_SUB_CMD

if TYPE_CHECKING:
    from pathlib import Path

    from click import Command


class TestCLI:
    @mark.parametrize(
        ("command", "args"),
        [
            # clean-dir
            param(actions.clean_dir.cli.cli, []),
            param(actions.clean_dir.cli.cli, ["--path", str(TEMP_DIR)]),
            param(actions.cli.cli, [CLEAN_DIR_SUB_CMD]),
            # publish-package
            param(actions.publish_package.cli.cli, []),
            param(actions.publish_package.cli.cli, ["--username", "username"]),
            param(actions.cli.cli, [PUBLISH_PACKAGE_SUB_CMD]),
            # random-sleep
            param(actions.random_sleep.cli.cli, []),
            param(actions.cli.cli, [RANDOM_SLEEP_SUB_CMD]),
            # set-up-cron
            param(actions.set_up_cron.cli.cli, ["name", "command"]),
            param(actions.cli.cli, [SET_UP_CRON_SUB_CMD, "name", "command"]),
            # tag-commit
            param(actions.tag_commit.cli.cli, []),
            param(actions.cli.cli, [TAG_COMMIT_SUB_CMD]),
        ],
    )
    @throttle_test(duration=MINUTE)
    def test_commands(self, *, command: Command, args: list[str]) -> None:
        runner = CliRunner()
        result = runner.invoke(command, args)
        assert result.exit_code == 0, result.stderr

    @mark.parametrize(
        ("command", "args"),
        [
            param(actions.re_encrypt.cli.cli, []),
            param(actions.cli.cli, [RE_ENCRYPT_SUB_CMD]),
        ],
    )
    @throttle_test(duration=MINUTE)
    def test_re_encrypt(
        self, *, command: Command, args: list[str], tmp_path: Path
    ) -> None:
        path = tmp_path / "secrets.json"
        path.touch()
        runner = CliRunner()
        result = runner.invoke(command, [*args, str(path)])
        assert result.exit_code == 0, result.stderr

    @mark.parametrize(
        ("command", "args"),
        [
            param(actions.register_gitea_runner.cli.cli, []),
            param(actions.cli.cli, [REGISTER_GITEA_RUNNER_SUB_CMD]),
        ],
    )
    @throttle_test(duration=MINUTE)
    def test_register_gitea_runner(
        self, *, command: Command, args: list[str], tmp_path: Path
    ) -> None:
        path = tmp_path / "secrets.json"
        path.touch()
        runner = CliRunner()
        result = runner.invoke(command, [*args, "--runner-certificate", str(path)])
        assert result.exit_code == 0, result.stderr

    @mark.parametrize("head", [param([]), param(["just"], marks=skipif_ci)])
    @mark.parametrize(
        "command",
        [
            param("clean-dir"),
            param("cli"),
            param("publish-package"),
            param("random-sleep"),
            param("re-encrypt"),
            param("register-gitea-runner"),
            param("set-up-cron"),
            param("tag-commit"),
        ],
    )
    @throttle_test(duration=MINUTE)
    def test_entrypoints_and_justfile(self, *, head: list[str], command: str) -> None:
        run(*head, command, "--help")
