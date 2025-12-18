from __future__ import annotations

from typed_settings import Secret, option, secret, settings


@settings
class Settings:
    token: Secret[str] | None = secret(default=None, help="GitHub token")
    flag: bool = option(default=False, help="Example flag")
    dry_run: bool = option(default=False, help="Dry run the CLI")


SETTINGS = Settings()


__all__ = ["SETTINGS", "Settings"]
