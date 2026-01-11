from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.atomicwrites import writer

from actions.constants import SSH
from actions.logging import LOGGER
from actions.utilities import log_func_call

if TYPE_CHECKING:
    from pathlib import Path


def setup_ssh_config() -> None:
    LOGGER.info(log_func_call(setup_ssh_config))
    path = get_ssh_config("*")
    with writer(SSH / "config", overwrite=True) as temp:
        _ = temp.write_text(f"Include {path}")
    path.parent.mkdir(parents=True, exist_ok=True)


def get_ssh_config(stem: str, /) -> Path:
    return SSH / "config.d" / f"{stem}.conf"


__all__ = ["setup_ssh_config"]
