from __future__ import annotations

from contextlib import suppress
from os import environ
from pathlib import Path

from utilities.constants import CPU_COUNT, HOSTNAME, SYSTEM, USER

import actions.constants
from actions.constants import PATH_ACTIONS

GITEA_HOST = "gitea.main"
GITEA_PORT = 3000


GITEA_CONTAINER_USER = "git"
GITEA_CONTAINER_NAME = "gitea"


REGISTER_GITEA_RUNNER_SUB_CMD = "register-gitea-runner"
REGISTER_GITEA_RUNNER_DOCSTRING = "Register a Gitea runner"


PATH_CACHE = actions.constants.PATH_CACHE / REGISTER_GITEA_RUNNER_SUB_CMD
PATH_CONFIGS = PATH_ACTIONS / "register_gitea_runner/configs"
PATH_WAIT_FOR_IT = PATH_CACHE / "wait-for-it.sh"
URL_WAIT_FOR_IT = "https://raw.githubusercontent.com/vishnubob/wait-for-it/refs/heads/master/wait-for-it.sh"


def _get_runner_instance_name() -> str:
    parts: list[str] = [USER, HOSTNAME]
    with suppress(KeyError):
        parts.append(environ["SUBNET"])
    return "--".join(parts).lower()


RUNNER_CAPACITY = max(round(3 * CPU_COUNT / 4), 1)
RUNNER_CERTIFICATE = Path("root.pem")
RUNNER_CONTAINER_NAME = "runner"
RUNNER_INSTANCE_NAME = _get_runner_instance_name()
RUNNER_LABELS = [f"host-{SYSTEM}"]


SSH_USER = "nonroot"
SSH_HOST = "gitea.main"


__all__ = [
    "GITEA_CONTAINER_NAME",
    "GITEA_CONTAINER_USER",
    "GITEA_HOST",
    "GITEA_PORT",
    "PATH_CACHE",
    "PATH_CONFIGS",
    "PATH_WAIT_FOR_IT",
    "REGISTER_GITEA_RUNNER_DOCSTRING",
    "REGISTER_GITEA_RUNNER_SUB_CMD",
    "RUNNER_CAPACITY",
    "RUNNER_CERTIFICATE",
    "RUNNER_CONTAINER_NAME",
    "RUNNER_INSTANCE_NAME",
    "RUNNER_LABELS",
    "SSH_HOST",
    "SSH_USER",
    "URL_WAIT_FOR_IT",
]
