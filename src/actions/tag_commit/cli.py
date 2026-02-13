from __future__ import annotations

from typing import TYPE_CHECKING

from click import Command, command
from utilities.click import CONTEXT_SETTINGS, Str, option
from utilities.core import is_pytest, set_up_logging

from actions import __version__
from actions.tag_commit.constants import USER_EMAIL, USER_NAME
from actions.tag_commit.lib import tag_commit

if TYPE_CHECKING:
    from collections.abc import Callable


TAG_COMMIT_SUB_CMD = "tag-commit"


def make_tag_commit_cmd(
    *, cli: Callable[..., Command] = command, name: str | None = None
) -> Command:
    @option("--user-name", type=Str(), default=USER_NAME, help="'git' user name")
    @option("--user-email", type=Str(), default=USER_EMAIL, help="'git' user email")
    @option(
        "--major-minor", is_flag=True, default=False, help="Add the 'major.minor' tag"
    )
    @option("--major", is_flag=True, default=False, help="Add the 'major' tag")
    @option("--latest", is_flag=True, default=False, help="Add the 'latest' tag")
    def func(
        *, user_name: str, user_email: str, major_minor: bool, major: bool, latest: bool
    ) -> None:
        if is_pytest():
            return
        set_up_logging(__name__, root=True, log_version=__version__)
        tag_commit(
            user_name=user_name,
            user_email=user_email,
            major_minor=major_minor,
            major=major,
            latest=latest,
        )

    return cli(name=name, help="Tag the latest commit", **CONTEXT_SETTINGS)(func)


cli = make_tag_commit_cmd()


__all__ = ["TAG_COMMIT_SUB_CMD", "cli", "make_tag_commit_cmd"]
