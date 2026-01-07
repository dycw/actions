from __future__ import annotations

from pathlib import Path
from re import search

from utilities.pathlib import get_repo_root
from utilities.pytest import IS_CI

from actions.pre_commit.constants import PATH_PRE_COMMIT

ACTIONS_URL = "https://github.com/dycw/actions"
DOCKERFMT_URL = "https://github.com/reteps/dockerfmt"
PRE_COMMIT_HOOKS_URL = "https://github.com/pre-commit/pre-commit-hooks"
RUFF_URL = "https://github.com/astral-sh/ruff-pre-commit"
SHELLCHECK_URL = "https://github.com/koalaman/shellcheck-precommit"
SHFMT_URL = "https://github.com/scop/pre-commit-shfmt"
TAPLO_URL = "https://github.com/compwa/taplo-pre-commit"
UV_URL = "https://github.com/astral-sh/uv-pre-commit"


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


CONFORMALIZE_REPO_SUB_CMD = "conformalize-repo"


MAX_PYTHON_VERSION = "3.14"


RUN_VERSION_BUMP = (search("template", str(REPO_ROOT)) is None) and not IS_CI


GITHUB_WORKFLOWS = Path(".github/workflows")
GITHUB_PULL_REQUEST_YAML = GITHUB_WORKFLOWS / "pull-request.yaml"
GITHUB_PUSH_YAML = GITHUB_WORKFLOWS / "push.yaml"
PATH_CONFIGS = PATH_PRE_COMMIT / "conformalize_repo/configs"


__all__ = [
    "ACTIONS_URL",
    "BUMPVERSION_TOML",
    "CONFORMALIZE_REPO_SUB_CMD",
    "COVERAGERC_TOML",
    "DOCKERFMT_URL",
    "ENVRC",
    "GITHUB_PULL_REQUEST_YAML",
    "GITHUB_PUSH_YAML",
    "GITHUB_WORKFLOWS",
    "GITIGNORE",
    "MAX_PYTHON_VERSION",
    "PATH_CONFIGS",
    "PRE_COMMIT_CONFIG_YAML",
    "PRE_COMMIT_HOOKS_URL",
    "PYPROJECT_TOML",
    "PYRIGHTCONFIG_JSON",
    "PYTEST_TOML",
    "README_MD",
    "REPO_ROOT",
    "RUFF_TOML",
    "RUFF_URL",
    "RUN_VERSION_BUMP",
    "SHELLCHECK_URL",
    "SHFMT_URL",
    "TAPLO_URL",
    "UV_URL",
]
