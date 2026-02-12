from __future__ import annotations

from click import group, version_option
from utilities.click import CONTEXT_SETTINGS

from actions import __version__
from actions.clean_dir.cli import CLEAN_DIR_SUB_CMD, make_clean_dir_cmd
from actions.publish_package.cli import (
    PUBLISH_PACKAGE_SUB_CMD,
    make_publish_package_cmd,
)
from actions.random_sleep.cli import RANDOM_SLEEP_SUB_CMD, make_random_sleep_cmd
from actions.re_encrypt.cli import RE_ENCRYPT_SUB_CMD, make_re_encrypt_cmd
from actions.register_gitea_runner.cli import make_register_gitea_runner_cmd
from actions.register_gitea_runner.constants import REGISTER_GITEA_RUNNER_SUB_CMD
from actions.set_up_cron.cli import SET_UP_CRON_SUB_CMD, make_set_up_cron_cmd
from actions.tag_commit.cli import TAG_COMMIT_SUB_CMD, make_tag_commit_cmd


@group(**CONTEXT_SETTINGS)
@version_option(version=__version__)
def cli() -> None: ...


_ = make_clean_dir_cmd(cli=cli.command, name=CLEAN_DIR_SUB_CMD)
_ = make_publish_package_cmd(cli=cli.command, name=PUBLISH_PACKAGE_SUB_CMD)
_ = make_random_sleep_cmd(cli=cli.command, name=RANDOM_SLEEP_SUB_CMD)
_ = make_re_encrypt_cmd(cli=cli.command, name=RE_ENCRYPT_SUB_CMD)
_ = make_register_gitea_runner_cmd(cli=cli.command, name=REGISTER_GITEA_RUNNER_SUB_CMD)
_ = make_set_up_cron_cmd(cli=cli.command, name=SET_UP_CRON_SUB_CMD)
_ = make_tag_commit_cmd(cli=cli.command, name=TAG_COMMIT_SUB_CMD)


if __name__ == "__main__":
    cli()
