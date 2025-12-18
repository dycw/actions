from __future__ import annotations

from subprocess import check_output

from actions.logging import LOGGER


def log_run(*cmds: str) -> str:
    LOGGER.info("Running '%s'...", " ".join(cmds))
    return check_output(cmds, text=True)


__all__ = ["log_run"]
