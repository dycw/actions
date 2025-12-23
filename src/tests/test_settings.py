from __future__ import annotations

from typed_settings import load_settings
from utilities.os import temp_environ

from actions.settings import CommonSettings
from actions.utilities import LOADER


class TestCommonSettings:
    def test_empty_strs(self) -> None:
        with temp_environ(TOKEN=""):
            settings = load_settings(CommonSettings, [LOADER])
        assert settings.token is None
