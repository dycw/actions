from __future__ import annotations

from typed_settings import load_settings
from utilities.os import temp_environ

from actions.publish.settings import PublishSettings
from actions.utilities import LOADER


class TestSettings:
    def test_empty_strs(self) -> None:
        with temp_environ(USERNAME="", PASSWORD="", PUBLISH_URL=""):
            settings = load_settings(PublishSettings, [LOADER])
        assert settings.username is None
        assert settings.password is None
        assert settings.publish_url is None
