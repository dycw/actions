from __future__ import annotations

from typed_settings import click_options
from utilities.core import is_pytest
from utilities.logging import basic_config

from actions.logging import LOGGER
from actions.tag_commit.lib import tag_commit
from actions.tag_commit.settings import Settings
from actions.utilities import LOADER


@click_options(Settings, [LOADER], show_envvars_in_help=True)
def tag_commit_sub_cmd(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    tag_commit(
        user_name=settings.user_name,
        user_email=settings.user_email,
        major_minor=settings.major_minor,
        major=settings.major,
        latest=settings.latest,
    )


__all__ = ["tag_commit_sub_cmd"]
