from __future__ import annotations

from re import search

from utilities.pytest import IS_CI

from actions.constants import REPO_ROOT
from actions.pre_commit.constants import PATH_PRE_COMMIT

DOCKERFMT_URL = "https://github.com/reteps/dockerfmt"
PRE_COMMIT_HOOKS_URL = "https://github.com/pre-commit/pre-commit-hooks"
RUFF_URL = "https://github.com/astral-sh/ruff-pre-commit"
SHELLCHECK_URL = "https://github.com/koalaman/shellcheck-precommit"
SHFMT_URL = "https://github.com/scop/pre-commit-shfmt"
TAPLO_URL = "https://github.com/compwa/taplo-pre-commit"
UV_URL = "https://github.com/astral-sh/uv-pre-commit"


CONFORMALIZE_REPO_DOCSTRING = "Conformalize a repo"
CONFORMALIZE_REPO_SUB_CMD = "conformalize-repo"


PATH_CONFIGS = PATH_PRE_COMMIT / "conformalize_repo/configs"


RUN_VERSION_BUMP = (search("template", str(REPO_ROOT)) is None) and not IS_CI


__all__ = [
    "CONFORMALIZE_REPO_DOCSTRING",
    "CONFORMALIZE_REPO_SUB_CMD",
    "DOCKERFMT_URL",
    "PATH_CONFIGS",
    "PRE_COMMIT_HOOKS_URL",
    "REPO_ROOT",
    "RUFF_URL",
    "RUN_VERSION_BUMP",
    "SHELLCHECK_URL",
    "SHFMT_URL",
    "TAPLO_URL",
    "UV_URL",
]
