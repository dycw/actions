from __future__ import annotations

from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.sops.lib import setup_sops


def sops_sub_cmd() -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s)...
        """),
        setup_sops.__name__,
        __version__,
    )
    setup_sops()


__all__ = ["sops_sub_cmd"]
