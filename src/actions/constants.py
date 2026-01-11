from __future__ import annotations

from pathlib import Path

from ruamel.yaml import YAML
from utilities.importlib import files
from xdg_base_dirs import xdg_cache_home

ACTIONS_URL = "https://github.com/dycw/actions"


BUMPVERSION_TOML = Path(".bumpversion.toml")
COVERAGERC_TOML = Path(".coveragerc.toml")
ENVRC = Path(".envrc")
GITEA = Path(".gitea")
GITHUB = Path(".github")
GITIGNORE = Path(".gitignore")
PRE_COMMIT_CONFIG_YAML = Path(".pre-commit-config.yaml")
PYPROJECT_TOML = Path("pyproject.toml")
PYRIGHTCONFIG_JSON = Path("pyrightconfig.json")
PYTEST_TOML = Path("pytest.toml")
README_MD = Path("README.md")
SSH = Path.home() / ".ssh"
RUFF_TOML = Path("ruff.toml")


GITHUB_WORKFLOWS, GITEA_WORKFLOWS = [g / "workflows" for g in [GITHUB, GITEA]]
GITHUB_PULL_REQUEST_YAML, GITEA_PULL_REQUEST_YAML = [
    w / "pull-request.yaml" for w in [GITHUB_WORKFLOWS, GITEA_WORKFLOWS]
]
GITHUB_PUSH_YAML, GITEA_PUSH_YAML = [
    w / "push.yaml" for w in [GITHUB_WORKFLOWS, GITEA_WORKFLOWS]
]


MAX_PYTHON_VERSION = "3.14"


PATH_ACTIONS = files(anchor="actions")
PATH_CACHE = xdg_cache_home() / "actions"


YAML_INSTANCE = YAML()


__all__ = [
    "ACTIONS_URL",
    "BUMPVERSION_TOML",
    "COVERAGERC_TOML",
    "ENVRC",
    "GITEA",
    "GITEA_PUSH_YAML",
    "GITEA_WORKFLOWS",
    "GITHUB",
    "GITHUB_PULL_REQUEST_YAML",
    "GITHUB_PUSH_YAML",
    "GITHUB_WORKFLOWS",
    "GITHUB_WORKFLOWS",
    "GITIGNORE",
    "MAX_PYTHON_VERSION",
    "PATH_ACTIONS",
    "PATH_CACHE",
    "PRE_COMMIT_CONFIG_YAML",
    "PYPROJECT_TOML",
    "PYRIGHTCONFIG_JSON",
    "PYTEST_TOML",
    "README_MD",
    "RUFF_TOML",
    "SSH",
    "YAML_INSTANCE",
]
