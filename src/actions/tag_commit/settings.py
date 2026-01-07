from __future__ import annotations

from typed_settings import load_settings, option, settings

from actions.utilities import LOADER


@settings
class Settings:
    user_name: str = option(default="github-actions-bot", help="'git' user name")
    user_email: str = option(default="noreply@github.com", help="'git' user email")
    major_minor: bool = option(default=False, help="Add the 'major.minor' tag")
    major: bool = option(default=False, help="Add the 'major' tag")
    latest: bool = option(default=False, help="Add the 'latest' tag")


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["SETTINGS", "Settings"]
