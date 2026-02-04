from __future__ import annotations

from actions.constants import PATH_ACTIONS

KILL_AFTER = 10
LOGS_KEEP = 7
SCHEDULE = "* * * * *"
SUDO = False
TIMEOUT = 60


PATH_CONFIGS = PATH_ACTIONS / "setup_cronjob/configs"


SETUP_CRONJOB_SUB_CMD = "setup-cronjob"
SETUP_CRONJOB_DOCSTRING = "Setup a cronjob"


__all__ = [
    "KILL_AFTER",
    "LOGS_KEEP",
    "PATH_CONFIGS",
    "SCHEDULE",
    "SETUP_CRONJOB_DOCSTRING",
    "SETUP_CRONJOB_SUB_CMD",
    "SUDO",
    "TIMEOUT",
]
