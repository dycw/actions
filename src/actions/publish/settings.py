from __future__ import annotations

from typed_settings import Secret, load_settings, option, secret, settings

from actions.utilities import ENV_LOADER, empty_str_to_none


@settings
class PublishSettings:
    token: Secret[str] | None = secret(
        default=None, converter=empty_str_to_none, help="GitHub token"
    )
    username: str | None = option(
        default=None, converter=empty_str_to_none, help="The username of the upload"
    )
    password: Secret[str] | None = secret(
        default=None, converter=empty_str_to_none, help="The password for the upload"
    )
    publish_url: str | None = option(
        default=None, converter=empty_str_to_none, help="The URL of the upload endpoint"
    )
    trusted_publishing: bool = option(
        default=False, help="Configure trusted publishing"
    )
    native_tls: bool = option(
        default=False,
        help="Whether to load TLS certificates from the platform's native certificate store",
    )
    dry_run: bool = option(default=False, help="Dry run the CLI")


PUBLISH_SETTINGS = load_settings(PublishSettings, [ENV_LOADER])


__all__ = ["PUBLISH_SETTINGS", "PublishSettings"]
