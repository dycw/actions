from __future__ import annotations

from ruamel.yaml import YAML
from utilities.importlib import files

PATH_ACTIONS = files(anchor="actions")
YAML_INSTANCE = YAML()


__all__ = ["PATH_ACTIONS", "YAML_INSTANCE"]
