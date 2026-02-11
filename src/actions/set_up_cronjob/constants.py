from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.constants import MINUTE, SECOND

from actions.constants import PATH_ACTIONS

if TYPE_CHECKING:
    from pathlib import Path

    from utilities.types import Duration

KILL_AFTER: Duration = 10 * SECOND
LOGS_KEEP: int = 7
SCHEDULE: str = "* * * * *"
TIMEOUT: Duration = MINUTE


PATH_CONFIGS: Path = PATH_ACTIONS / "set_up_cronjob/configs"


SET_UP_CRONJOB_SUB_CMD: str = "set-up-cronjob"
SET_UP_CRONJOB_DOCSTRING: str = "Set up a cronjob"


__all__ = [
    "KILL_AFTER",
    "LOGS_KEEP",
    "PATH_CONFIGS",
    "SCHEDULE",
    "SET_UP_CRONJOB_DOCSTRING",
    "SET_UP_CRONJOB_SUB_CMD",
    "TIMEOUT",
]
