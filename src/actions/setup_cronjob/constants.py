from __future__ import annotations

from actions.constants import PATH_ACTIONS

PATH_CONFIGS = PATH_ACTIONS / "setup_cronjob/configs"


SETUP_CRONJOB_SUB_CMD = "setup-cronjob"
SETUP_CRONJOB_DOCSTRING = "Setup a cronjob"


KILL_AFTER = 10
LOGS_KEEP = 7
SCHEDULE = "* * * * *"
TIMEOUT = 60


__all__ = [
    "KILL_AFTER",
    "LOGS_KEEP",
    "PATH_CONFIGS",
    "SCHEDULE",
    "SETUP_CRONJOB_DOCSTRING",
    "SETUP_CRONJOB_SUB_CMD",
    "TIMEOUT",
]
