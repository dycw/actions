from __future__ import annotations

from typed_settings import click_options
from utilities.core import is_pytest
from utilities.logging import basic_config

from actions.logging import LOGGER
from actions.publish_package.lib import publish_package
from actions.publish_package.settings import Settings
from actions.utilities import LOADER


@click_options(Settings, [LOADER], show_envvars_in_help=True)
def publish_package_sub_cmd(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    publish_package(
        username=settings.username,
        password=settings.password,
        publish_url=settings.publish_url,
        trusted_publishing=settings.trusted_publishing,
        native_tls=settings.native_tls,
    )


__all__ = ["publish_package_sub_cmd"]
