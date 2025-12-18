from __future__ import annotations

from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.logging import basic_config

from actions import __version__
from actions.logging import LOGGER
from actions.publish.lib import publish_package
from actions.publish.settings import PublishSettings
from actions.settings import CommonSettings
from actions.utilities import ENV_LOADER


@click_options(
    CommonSettings, [ENV_LOADER], show_envvars_in_help=True, argname="common"
)
@click_options(
    PublishSettings, [ENV_LOADER], show_envvars_in_help=True, argname="publish"
)
def publish_sub_cmd(*, common: CommonSettings, publish: PublishSettings) -> None:
    basic_config(obj=LOGGER)
    LOGGER.info(
        """\
Running '%r' (version %s) with settings:
%s
%s""",
        publish_package.__name__,
        __version__,
        pretty_repr(common),
        pretty_repr(publish),
    )
    if common.dry_run:
        LOGGER.info("Dry run; exiting...")
        return
    publish_package(
        username=publish.username,
        password=publish.password,
        publish_url=publish.publish_url,
        trusted_publishing=publish.trusted_publishing,
        native_tls=publish.native_tls,
    )


__all__ = ["publish_sub_cmd"]
