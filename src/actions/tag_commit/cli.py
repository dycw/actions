from __future__ import annotations

from click import option
from utilities.click import Str
from utilities.core import is_pytest
from utilities.logging import basic_config

from actions.logging import LOGGER
from actions.tag_commit.constants import USER_EMAIL, USER_NAME
from actions.tag_commit.lib import tag_commit


@option("--user_name", type=Str(), default=USER_NAME, help="'git' user name")
@option("--user_email", type=Str(), default=USER_EMAIL, help="'git' user email")
@option("--major_minor", is_flag=True, default=False, help="Add the 'major.minor' tag")
@option("--major", is_flag=True, default=False, help="Add the 'major' tag")
@option("--latest", is_flag=True, default=False, help="Add the 'latest' tag")
def tag_commit_sub_cmd(
    *, user_name: str, user_email: str, major_minor: bool, major: bool, latest: bool
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    tag_commit(
        user_name=user_name,
        user_email=user_email,
        major_minor=major_minor,
        major=major,
        latest=latest,
    )


__all__ = ["tag_commit_sub_cmd"]
