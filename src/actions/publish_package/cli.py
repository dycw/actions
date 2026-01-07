from __future__ import annotations

from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.publish_package.lib import publish_package
from actions.publish_package.settings import PublishSettings
from actions.utilities import LOADER


@click_options(PublishSettings, [LOADER], show_envvars_in_help=True, argname="publish")
def publish_package_sub_cmd(*, publish: PublishSettings) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
            %s
        """),
        publish_package.__name__,
        __version__,
        pretty_repr(publish),
    )
    publish_package(
        username=publish.username,
        password=publish.password,
        publish_url=publish.publish_url,
        trusted_publishing=publish.trusted_publishing,
        native_tls=publish.native_tls,
    )


__all__ = ["publish_package_sub_cmd"]
