from __future__ import annotations

from subprocess import check_output

from typed_settings import EnvLoader

from actions.logging import LOGGER

ENV_LOADER = EnvLoader("")


def empty_str_to_none(text: str, /) -> str | None:
    return None if text == "" else text


def log_run(*cmds: str) -> str:
    LOGGER.info("Running '%s'...", " ".join(cmds))
    return check_output(cmds, text=True)


__all__ = ["ENV_LOADER", "empty_str_to_none", "log_run"]
