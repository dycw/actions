from __future__ import annotations

from subprocess import check_output

from typed_settings import EnvLoader, Secret

from actions.logging import LOGGER

ENV_LOADER = EnvLoader("")


def empty_str_to_none(text: str, /) -> str | None:
    return None if text == "" else text


def log_run(*cmds: str | Secret[str]) -> str:
    LOGGER.info("Running '%s'...", " ".join(map(str, cmds)))
    return check_output(
        [c if isinstance(c, str) else c.get_secret_value() for c in cmds], text=True
    ).rstrip("\n")


__all__ = ["ENV_LOADER", "empty_str_to_none", "log_run"]
