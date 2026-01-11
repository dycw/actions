from __future__ import annotations

from utilities.atomicwrites import writer

from actions.constants import SSH
from actions.logging import LOGGER
from actions.utilities import log_func_call


def setup_ssh_config() -> None:
    LOGGER.info(log_func_call(setup_ssh_config))
    with writer(SSH / "config") as temp:
        _ = temp.write_text(f"Include {SSH}/config.d/*.conf")
    (SSH / "config.d").mkdir(parents=True, exist_ok=True)


__all__ = ["setup_ssh_config"]
