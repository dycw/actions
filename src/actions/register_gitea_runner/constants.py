from __future__ import annotations

import actions.constants
from actions.constants import PATH_ACTIONS

REGISTER_GITEA_RUNNER_SUB_CMD = "register-gitea-runner"
REGISTER_GITEA_RUNNER_DOCSTRING = "Register a Gitea runner"


PATH_CACHE = actions.constants.PATH_CACHE / REGISTER_GITEA_RUNNER_SUB_CMD
PATH_CONFIGS = PATH_ACTIONS / "register_gitea_runner/configs"
PATH_WAIT_FOR_IT = PATH_CACHE / "wait-for-it.sh"
URL_WAIT_FOR_IT = "https://raw.githubusercontent.com/vishnubob/wait-for-it/refs/heads/master/wait-for-it.sh"


__all__ = [
    "PATH_CACHE",
    "PATH_CONFIGS",
    "PATH_WAIT_FOR_IT",
    "REGISTER_GITEA_RUNNER_DOCSTRING",
    "REGISTER_GITEA_RUNNER_SUB_CMD",
    "URL_WAIT_FOR_IT",
]
