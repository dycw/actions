from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.tempfile import TemporaryDirectory
from utilities.text import strip_and_dedent

from actions import __version__
from actions.hooks.settings import HOOKS_SETTINGS
from actions.logging import LOGGER
from actions.utilities import log_run

if TYPE_CHECKING:
    from typed_settings import Secret


def hooks_package(
    *,
    repos: list[str] | None = HOOKS_SETTINGS.repos,
    hooks: list[str] | None = HOOKS_SETTINGS.hooks,
) -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - username           = %s
             - password           = %s
             - hooks_url        = %s
             - trusted_hooksing = %s
             - native_tls         = %s
        """),
        hooks_package.__name__,
        __version__,
        hooks,
        password,
        hooks_url,
        trusted_hooksing,
        native_tls,
    )
    with TemporaryDirectory() as temp:
        log_run("uv", "build", "--out-dir", str(temp), "--wheel", "--clear")
        log_run(
            "uv",
            "hooks",
            *([] if hooks is None else ["--username", hooks]),
            *([] if password is None else ["--password", password]),
            *([] if hooks_url is None else ["--hooks-url", hooks_url]),
            *(["--trusted-hooksing", "always"] if trusted_hooksing else []),
            *(["--native-tls"] if native_tls else []),
            f"{temp}/*",
        )


__all__ = ["hooks_package"]
