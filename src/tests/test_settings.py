from __future__ import annotations

from typed_settings import EnvLoader, load_settings
from utilities.os import temp_environ

from actions.settings import CommonSettings


class TestCommonSettings:
    def test_empty_strs(self) -> None:
        with temp_environ(TOKEN=""):
            settings = load_settings(CommonSettings, [EnvLoader("")])
        assert settings.token is None
