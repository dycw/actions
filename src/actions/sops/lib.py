from __future__ import annotations

from typing import TYPE_CHECKING, assert_never

from utilities.platform import SYSTEM
from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER

if TYPE_CHECKING:
    from typed_settings import Secret


def setup_sops(*, token: Secret[str] | None = None) -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - token = %s
        """),
        setup_sops.__name__,
        __version__,
        token,
    )
    match SYSTEM:
        case "linux":
            raise NotImplementedError
        case "mac":
            raise NotImplementedError
        case "windows":
            raise NotImplementedError
        case never:
            assert_never(never)
