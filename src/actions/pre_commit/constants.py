from __future__ import annotations

from utilities.constants import HOUR

from actions.constants import PATH_ACTIONS

PATH_PRE_COMMIT = PATH_ACTIONS / "pre_commit"
THROTTLE_DURATION = 12 * HOUR


__all__ = ["PATH_PRE_COMMIT", "THROTTLE_DURATION"]
