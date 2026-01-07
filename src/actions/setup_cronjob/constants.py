from __future__ import annotations

from actions.constants import PATH_ACTIONS

PATH_CONFIGS = PATH_ACTIONS / "setup_cronjob/configs"


SETUP_CRONJOB_SUB_CMD = "setup-cronjob"
SETUP_CRONJOB_DOCSTRING = "Setup a cronjob"


__all__ = ["PATH_CONFIGS", "SETUP_CRONJOB_DOCSTRING", "SETUP_CRONJOB_SUB_CMD"]
