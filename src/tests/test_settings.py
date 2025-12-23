from __future__ import annotations

from typed_settings import load_settings

from actions.settings import CommonSettings
from actions.utilities import LOADER


class TestCommonSettings:
    def test_empty_strs(self) -> None:
        settings = load_settings(CommonSettings, [LOADER])
        assert settings.token is None
