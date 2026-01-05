from __future__ import annotations

from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER


def setup_sops() -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s)...
        """),
        setup_sops.__name__,
        __version__,
    )
