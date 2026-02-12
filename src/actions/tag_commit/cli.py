from __future__ import annotations

from click import command, option
from utilities.click import CONTEXT_SETTINGS, Str
from utilities.core import is_pytest, set_up_logging

from actions.tag_commit.constants import TAG_COMMIT_DOCSTRING, USER_EMAIL, USER_NAME
from actions.tag_commit.lib import tag_commit


@option("--user-name", type=Str(), default=USER_NAME, help="'git' user name")
@option("--user-email", type=Str(), default=USER_EMAIL, help="'git' user email")
@option("--major-minor", is_flag=True, default=False, help="Add the 'major.minor' tag")
@option("--major", is_flag=True, default=False, help="Add the 'major' tag")
@option("--latest", is_flag=True, default=False, help="Add the 'latest' tag")
def tag_commit_sub_cmd(
    *, user_name: str, user_email: str, major_minor: bool, major: bool, latest: bool
) -> None:
    if is_pytest():
        return
    set_up_logging(__name__, root=True)
    tag_commit(
        user_name=user_name,
        user_email=user_email,
        major_minor=major_minor,
        major=major,
        latest=latest,
    )


cli = command(help=TAG_COMMIT_DOCSTRING, **CONTEXT_SETTINGS)(tag_commit_sub_cmd)


__all__ = ["cli", "tag_commit_sub_cmd"]
