from __future__ import annotations

from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.logging import basic_config

from actions import __version__
from actions.logging import LOGGER
from actions.settings import CommonSettings
from actions.tag.lib import tag_commit
from actions.tag.settings import TagSettings
from actions.utilities import ENV_LOADER


@click_options(
    CommonSettings, [ENV_LOADER], show_envvars_in_help=True, argname="common"
)
@click_options(TagSettings, [ENV_LOADER], show_envvars_in_help=True, argname="tag")
def tag_sub_cmd(*, common: CommonSettings, tag: TagSettings) -> None:
    basic_config(obj=LOGGER)
    LOGGER.info(
        """\
Running '%r' (version %s) with settings:
%s
%s""",
        tag_commit.__name__,
        __version__,
        pretty_repr(common),
        pretty_repr(tag),
    )
    if common.dry_run:
        LOGGER.info("Dry run; exiting...")
        return
    tag_commit(
        user_name=tag.user_name,
        user_email=tag.user_email,
        major_minor=tag.major_minor,
        major=tag.major,
        latest=tag.latest,
    )


__all__ = ["tag_sub_cmd"]
