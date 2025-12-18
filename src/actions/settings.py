from __future__ import annotations

from typed_settings import Secret, option, secret, settings


def _converter(text: str, /) -> str | None:
    return None if text == "" else text


@settings
class Settings:
    token: Secret[str] | None = secret(
        default=None, converter=_converter, help="GitHub token"
    )
    dry_run: bool = option(default=False, help="Dry run the CLI")
    tag: _TagSettings = option(factory=lambda: _TagSettings(), help="'tag' settings")


@settings
class _TagSettings:
    user_name: str = option(default="github-actions-bot", help="'git' user name")
    user_email: str = option(default="noreply@github.com", help="'git' user email")
    major_minor: bool = option(default=False, help="Add the 'major.minor' tag")
    major: bool = option(default=False, help="Add the 'major' tag")
    latest: bool = option(default=False, help="Add the 'latest' tag")


SETTINGS = Settings()


__all__ = ["SETTINGS", "Settings"]
