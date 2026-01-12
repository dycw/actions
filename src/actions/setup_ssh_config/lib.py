from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.atomicwrites import writer
from utilities.functions import get_func_name
from utilities.tabulate import func_param_desc

from actions import __version__
from actions.constants import SSH
from actions.logging import LOGGER

if TYPE_CHECKING:
    from pathlib import Path


def setup_ssh_config() -> None:
    LOGGER.info(func_param_desc(setup_ssh_config, __version__))
    path = get_ssh_config("*")
    with writer(SSH / "config", overwrite=True) as temp:
        _ = temp.write_text(f"Include {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    LOGGER.info("Finished running %r", get_func_name(setup_ssh_config))


def get_ssh_config(stem: str, /) -> Path:
    return SSH / "config.d" / f"{stem}.conf"


__all__ = ["setup_ssh_config"]
