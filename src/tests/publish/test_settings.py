from __future__ import annotations

from typed_settings import load_settings

from actions.publish_package.settings import Settings
from actions.utilities import LOADER


class TestPublishSettings:
    def test_empty_strs(self) -> None:
        settings = load_settings(Settings, [LOADER])
        assert settings.username is None
        assert settings.password is None
        assert settings.publish_url is None
