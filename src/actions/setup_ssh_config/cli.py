from __future__ import annotations

from utilities.logging import basic_config
from utilities.os import is_pytest

from actions.logging import LOGGER
from actions.setup_ssh_config.lib import setup_ssh_config


def setup_ssh_config_sub_cmd() -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_ssh_config()


__all__ = ["setup_ssh_config_sub_cmd"]
