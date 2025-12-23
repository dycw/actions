from __future__ import annotations

from typing import TYPE_CHECKING, assert_never

from typed_settings import Secret, load_settings, option, secret, settings
from utilities.logging import basic_config

from actions.logging import LOGGER
from actions.utilities import LOADER, empty_str_to_none

if TYPE_CHECKING:
    from actions.types import SecretLike

basic_config(obj=LOGGER)


def empty_str_to_none2(value: SecretLike, /) -> Secret[str] | None:
    return empty_str_to_none(value)
    match value:
        case Secret():
            return value
        case str():
            return None if value == "" else Secret(value)
        case None:
            return None
        case never:
            assert_never(never)


@settings
class PublishSettings:
    username: str | None = option(
        default=None, converter=empty_str_to_none, help="The username of the upload"
    )
    password: Secret[str] | None = secret(
        default=None, converter=empty_str_to_none2, help="The password for the upload"
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


PUBLISH_SETTINGS = load_settings(PublishSettings, [LOADER])


__all__ = ["PUBLISH_SETTINGS", "PublishSettings"]
