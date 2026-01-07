from __future__ import annotations

from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.tag_commit.lib import tag_commit
from actions.tag_commit.settings import Settings
from actions.utilities import LOADER


@click_options(Settings, [LOADER], show_envvars_in_help=True, argname="tag")
def tag_commit_sub_cmd(*, tag: Settings) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
            %s
        """),
        tag_commit.__name__,
        __version__,
        pretty_repr(tag),
    )
    tag_commit(
        user_name=tag.user_name,
        user_email=tag.user_email,
        major_minor=tag.major_minor,
        major=tag.major,
        latest=tag.latest,
    )


__all__ = ["tag_commit_sub_cmd"]
