from __future__ import annotations

from subprocess import check_call

from typed_settings import EnvLoader, Secret

from actions.logging import LOGGER

ENV_LOADER = EnvLoader("")


def empty_str_to_none(text: str, /) -> str | None:
    return None if text == "" else text


def log_run(*cmds: str | Secret[str]) -> None:
    LOGGER.info("Running '%s'...", " ".join(map(str, cmds)))
    _ = check_call(
        [c if isinstance(c, str) else c.get_secret_value() for c in cmds], text=True
    )


__all__ = ["ENV_LOADER", "empty_str_to_none", "log_run"]
