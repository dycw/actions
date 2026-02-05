from __future__ import annotations

from ruamel.yaml import YAML
from utilities.click import flag
from utilities.importlib import files
from xdg_base_dirs import xdg_cache_home

PATH_ACTIONS = files(anchor="actions")
PATH_CACHE = xdg_cache_home() / "actions"
SUDO = False


YAML_INSTANCE = YAML()


sudo_option = flag("--sudo", default=SUDO, help="Run as 'sudo'")


__all__ = ["PATH_ACTIONS", "PATH_CACHE", "SUDO", "YAML_INSTANCE", "sudo_option"]
