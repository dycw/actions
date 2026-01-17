from __future__ import annotations

from pathlib import Path
from re import search

from utilities.constants import IS_CI
from utilities.pathlib import GetRootError, get_root

from actions.pre_commit.constants import PATH_PRE_COMMIT

BUILTIN = "builtin"
DOCKERFMT_URL = "https://github.com/reteps/dockerfmt"
PRE_COMMIT_HOOKS_URL = "https://github.com/pre-commit/pre-commit-hooks"
RUFF_URL = "https://github.com/astral-sh/ruff-pre-commit"
SHELLCHECK_URL = "https://github.com/koalaman/shellcheck-precommit"
SHFMT_URL = "https://github.com/scop/pre-commit-shfmt"
TAPLO_URL = "https://github.com/compwa/taplo-pre-commit"
UV_URL = "https://github.com/astral-sh/uv-pre-commit"


CONFORMALIZE_REPO_DOCSTRING = "Conformalize a repo"
CONFORMALIZE_REPO_SUB_CMD = "conformalize-repo"


FORMATTER_PRIORITY = 10
LINTER_PRIORITY = 20


PATH_CONFIGS = PATH_PRE_COMMIT / "conformalize_repo/configs"


try:
    root = get_root()
except GetRootError:
    root = Path.cwd()
RUN_VERSION_BUMP = all(not search("template", p) for p in root.parts) and not IS_CI


__all__ = [
    "BUILTIN",
    "CONFORMALIZE_REPO_DOCSTRING",
    "CONFORMALIZE_REPO_SUB_CMD",
    "DOCKERFMT_URL",
    "FORMATTER_PRIORITY",
    "LINTER_PRIORITY",
    "PATH_CONFIGS",
    "PRE_COMMIT_HOOKS_URL",
    "RUFF_URL",
    "RUN_VERSION_BUMP",
    "SHELLCHECK_URL",
    "SHFMT_URL",
    "TAPLO_URL",
    "UV_URL",
]
