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
    CommonSettings, [ENV_LOADER], show_envvars_in_help=True, argname="common_settings"
)
@click_options(
    TagSettings, [ENV_LOADER], show_envvars_in_help=True, argname="tag_settings"
)
def tag_sub_cmd(*, common_settings: CommonSettings, tag_settings: TagSettings) -> None:
    basic_config(obj=LOGGER)
    LOGGER.info(
        """\
Running version %s with settings:
%s
%s""",
        __version__,
        pretty_repr(common_settings),
        pretty_repr(tag_settings),
    )
    if common_settings.dry_run:
        LOGGER.info("Dry run; exiting...")
        return
    tag_commit(
        user_name=tag_settings.user_name,
        user_email=tag_settings.user_email,
        major_minor=tag_settings.major_minor,
        major=tag_settings.major,
        latest=tag_settings.latest,
    )


__all__ = ["tag_sub_cmd"]
