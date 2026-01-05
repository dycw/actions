from __future__ import annotations

from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.publish.lib import publish_package
from actions.publish.settings import PublishSettings
from actions.utilities import LOADER


@click_options(PublishSettings, [LOADER], show_envvars_in_help=True)
def publish_sub_cmd(settings: PublishSettings, /) -> None:
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
        pretty_repr(settings),
    )
    publish_package(
        username=settings.username,
        password=settings.password,
        publish_url=settings.publish_url,
        trusted_publishing=settings.trusted_publishing,
        native_tls=settings.native_tls,
    )


__all__ = ["publish_sub_cmd"]
