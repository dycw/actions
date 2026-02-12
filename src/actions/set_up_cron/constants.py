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


PATH_CONFIGS: Path = PATH_ACTIONS / "set_up_cron/configs"


__all__ = ["KILL_AFTER", "LOGS_KEEP", "PATH_CONFIGS", "SCHEDULE", "TIMEOUT"]
