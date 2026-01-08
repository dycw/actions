from __future__ import annotations

from ruamel.yaml import YAML
from utilities.importlib import files
from utilities.pathlib import get_repo_root
from xdg_base_dirs import xdg_cache_home

PATH_ACTIONS = files(anchor="actions")
PATH_CACHE = xdg_cache_home() / "actions"
PATH_THROTTLE_CACHE = PATH_CACHE / "throttle" / get_repo_root().name
YAML_INSTANCE = YAML()


__all__ = ["PATH_ACTIONS", "PATH_CACHE", "PATH_THROTTLE_CACHE", "YAML_INSTANCE"]
