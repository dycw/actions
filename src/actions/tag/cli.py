from __future__ import annotations

from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.tag.lib import tag_commit
from actions.tag.settings import TagSettings
from actions.utilities import LOADER


@click_options(TagSettings, [LOADER], show_envvars_in_help=True)
def tag_sub_cmd(settings: TagSettings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
            %s
            %s
        """),
        tag_commit.__name__,
        __version__,
        pretty_repr(settings),
    )
    tag_commit(
        user_name=settings.user_name,
        user_email=settings.user_email,
        major_minor=settings.major_minor,
        major=settings.major,
        latest=settings.latest,
    )


__all__ = ["tag_sub_cmd"]
