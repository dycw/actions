from __future__ import annotations

from typing import TYPE_CHECKING

from click.testing import CliRunner
from pytest import mark, param
from utilities.constants import MINUTE, TEMP_DIR
from utilities.pytest import skipif_ci, throttle_test
from utilities.subprocess import run

from actions.clean_dir.constants import CLEAN_DIR_SUB_CMD
from actions.cli import cli
from actions.publish_package.constants import PUBLISH_PACKAGE_SUB_CMD
from actions.random_sleep.constants import RANDOM_SLEEP_SUB_CMD
from actions.re_encrypt.constants import RE_ENCRYPT_SUB_CMD
from actions.register_gitea_runner.constants import REGISTER_GITEA_RUNNER_SUB_CMD
from actions.set_up_cronjob.constants import SET_UP_CRONJOB_SUB_CMD
from actions.tag_commit.constants import TAG_COMMIT_SUB_CMD

if TYPE_CHECKING:
    from pathlib import Path

    from utilities.types import SequenceStr


class TestCLI:
    @mark.parametrize(
        "commands",
        [
            param([CLEAN_DIR_SUB_CMD]),
            param([CLEAN_DIR_SUB_CMD, "--path", str(TEMP_DIR)]),
            param([PUBLISH_PACKAGE_SUB_CMD]),
            param([PUBLISH_PACKAGE_SUB_CMD, "--username", "username"]),
            param([RANDOM_SLEEP_SUB_CMD]),
            param([SET_UP_CRONJOB_SUB_CMD, "name", "command"]),
            param([TAG_COMMIT_SUB_CMD]),
        ],
    )
    @throttle_test(duration=MINUTE)
    def test_commands(self, *, commands: SequenceStr) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, commands)
        assert result.exit_code == 0, result.stderr

    @throttle_test(duration=MINUTE)
    def test_re_encrypt(self, *, tmp_path: Path) -> None:
        path = tmp_path / "secrets.json"
        path.touch()
        runner = CliRunner()
        result = runner.invoke(cli, [RE_ENCRYPT_SUB_CMD, str(path)])
        assert result.exit_code == 0, result.stderr

    @throttle_test(duration=MINUTE)
    def test_register_gitea_runner(self, *, tmp_path: Path) -> None:
        path = tmp_path / "secrets.json"
        path.touch()
        runner = CliRunner()
        result = runner.invoke(
            cli, [REGISTER_GITEA_RUNNER_SUB_CMD, "--runner-certificate", str(path)]
        )
        assert result.exit_code == 0, result.stderr

    def test_entrypoint(self) -> None:
        run("cli", "--help")

    @skipif_ci
    def test_justfile(self) -> None:
        run("just", "cli", "--help")
