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


PATH_CONFIGS: Path = PATH_ACTIONS / "setup_cronjob/configs"


SETUP_CRONJOB_SUB_CMD: str = "setup-cronjob"
SETUP_CRONJOB_DOCSTRING: str = "Setup a cronjob"


__all__ = [
    "KILL_AFTER",
    "LOGS_KEEP",
    "PATH_CONFIGS",
    "SCHEDULE",
    "SETUP_CRONJOB_DOCSTRING",
    "SETUP_CRONJOB_SUB_CMD",
    "TIMEOUT",
]
