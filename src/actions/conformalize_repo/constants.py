from __future__ import annotations

from pathlib import Path
from re import search

from utilities.pathlib import get_repo_root
from utilities.pytest import IS_CI

from actions.constants import PATH_ACTIONS

BUMPVERSION_TOML = Path(".bumpversion.toml")
COVERAGERC_TOML = Path(".coveragerc.toml")
ENVRC = Path(".envrc")
GITIGNORE = Path(".gitignore")
PRE_COMMIT_CONFIG_YAML = Path(".pre-commit-config.yaml")
PYPROJECT_TOML = Path("pyproject.toml")
PYRIGHTCONFIG_JSON = Path("pyrightconfig.json")
PYTEST_TOML = Path("pytest.toml")
README_MD = Path("README.md")
REPO_ROOT = get_repo_root()
RUFF_TOML = Path("ruff.toml")


MAX_PYTHON_VERSION = "3.14"


RUN_VERSION_BUMP = (search("template", str(REPO_ROOT)) is None) and not IS_CI


GITHUB_WORKFLOWS = Path(".github/workflows")
GITHUB_PULL_REQUEST_YAML = GITHUB_WORKFLOWS / "pull-request.yaml"
GITHUB_PUSH_YAML = GITHUB_WORKFLOWS / "push.yaml"
PATH_CONFIGS = PATH_ACTIONS / "conformalize_repo/configs"


__all__ = [
    "BUMPVERSION_TOML",
    "COVERAGERC_TOML",
    "ENVRC",
    "GITHUB_PULL_REQUEST_YAML",
    "GITHUB_PUSH_YAML",
    "GITHUB_WORKFLOWS",
    "GITIGNORE",
    "MAX_PYTHON_VERSION",
    "PATH_CONFIGS",
    "PRE_COMMIT_CONFIG_YAML",
    "PYPROJECT_TOML",
    "PYRIGHTCONFIG_JSON",
    "PYTEST_TOML",
    "README_MD",
    "REPO_ROOT",
    "RUFF_TOML",
    "RUN_VERSION_BUMP",
]
