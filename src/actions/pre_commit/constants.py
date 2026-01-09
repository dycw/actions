from __future__ import annotations

from utilities.whenever import HOUR

from actions.constants import PATH_ACTIONS

PATH_PRE_COMMIT = PATH_ACTIONS / "pre_commit"
THROTTLE_DELTA = 12 * HOUR


__all__ = ["PATH_PRE_COMMIT", "THROTTLE_DELTA"]
