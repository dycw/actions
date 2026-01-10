from __future__ import annotations

from pathlib import Path

from utilities.atomicwrites import writer

from actions.logging import LOGGER
from actions.utilities import log_func_call


def setup_ssh_config() -> None:
    LOGGER.info(log_func_call(setup_ssh_config))
    path = Path.home() / ".ssh"
    with writer(path / "config") as temp:
        _ = temp.write_text("Include ~/.ssh/config.d/*.conf")
    (path / "config.d").mkdir(parents=True, exist_ok=True)


__all__ = ["setup_ssh_config"]
