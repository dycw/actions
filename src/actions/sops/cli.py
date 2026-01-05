from __future__ import annotations

from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.sops.lib import setup_sops
from actions.sops.settings import SopsSettings
from actions.utilities import LOADER


@click_options(SopsSettings, [LOADER], show_envvars_in_help=True)
def sops_sub_cmd(settings: SopsSettings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
            %s
        """),
        setup_sops.__name__,
        __version__,
        pretty_repr(settings),
    )
    setup_sops(token=settings.token)


__all__ = ["sops_sub_cmd"]
