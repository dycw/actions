from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML
from utilities.importlib import files
from xdg_base_dirs import xdg_cache_home

PATH_ACTIONS = files(anchor="actions")
PATH_CACHE = xdg_cache_home() / "actions"


YAML_INSTANCE = YAML()


__all__ = ["PATH_ACTIONS", "PATH_CACHE", "YAML_INSTANCE"]
