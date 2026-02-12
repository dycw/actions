from __future__ import annotations

from click import group, version_option
from utilities.click import CONTEXT_SETTINGS

from actions import __version__
from actions.clean_dir.cli import clean_dir_sub_cmd
from actions.clean_dir.constants import CLEAN_DIR_DOCSTRING, CLEAN_DIR_SUB_CMD
from actions.publish_package.cli import (
    PUBLISH_PACKAGE_SUB_CMD,
    make_publish_package_cmd,
)
from actions.random_sleep.cli import random_sleep_sub_cmd
from actions.random_sleep.constants import RANDOM_SLEEP_DOCSTRING, RANDOM_SLEEP_SUB_CMD
from actions.re_encrypt.cli import re_encrypt_sub_cmd
from actions.re_encrypt.constants import RE_ENCRYPT_DOCSTRING, RE_ENCRYPT_SUB_CMD
from actions.register_gitea_runner.cli import register_gitea_runner_sub_cmd
from actions.register_gitea_runner.constants import (
    REGISTER_GITEA_RUNNER_DOCSTRING,
    REGISTER_GITEA_RUNNER_SUB_CMD,
)
from actions.set_up_cron.cli import setup_cronjob_sub_cmd
from actions.set_up_cron.constants import (
    SET_UP_CRONJOB_DOCSTRING,
    SET_UP_CRONJOB_SUB_CMD,
)
from actions.tag_commit.cli import tag_commit_sub_cmd
from actions.tag_commit.constants import TAG_COMMIT_DOCSTRING, TAG_COMMIT_SUB_CMD


@group(**CONTEXT_SETTINGS)
@version_option(version=__version__)
def cli() -> None: ...


_ = cli.command(name=CLEAN_DIR_SUB_CMD, help=CLEAN_DIR_DOCSTRING, **CONTEXT_SETTINGS)(
    clean_dir_sub_cmd
)
_ = make_publish_package_cmd(cli=cli.command, name=PUBLISH_PACKAGE_SUB_CMD)
_ = cli.command(
    name=RANDOM_SLEEP_SUB_CMD, help=RANDOM_SLEEP_DOCSTRING, **CONTEXT_SETTINGS
)(random_sleep_sub_cmd)
_ = cli.command(name=RE_ENCRYPT_SUB_CMD, help=RE_ENCRYPT_DOCSTRING, **CONTEXT_SETTINGS)(
    re_encrypt_sub_cmd
)
_ = cli.command(
    name=REGISTER_GITEA_RUNNER_SUB_CMD,
    help=REGISTER_GITEA_RUNNER_DOCSTRING,
    **CONTEXT_SETTINGS,
)(register_gitea_runner_sub_cmd)
_ = cli.command(
    name=SET_UP_CRONJOB_SUB_CMD, help=SET_UP_CRONJOB_DOCSTRING, **CONTEXT_SETTINGS
)(setup_cronjob_sub_cmd)
_ = cli.command(name=TAG_COMMIT_SUB_CMD, help=TAG_COMMIT_DOCSTRING, **CONTEXT_SETTINGS)(
    tag_commit_sub_cmd
)


if __name__ == "__main__":
    cli()
