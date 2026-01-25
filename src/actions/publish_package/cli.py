from __future__ import annotations

from typing import TYPE_CHECKING

from click import option
from utilities.click import Str
from utilities.core import is_pytest
from utilities.logging import basic_config

from actions.logging import LOGGER
from actions.publish_package.lib import publish_package

if TYPE_CHECKING:
    from utilities.pydantic import SecretLike


@option("--username", type=Str(), default=None, help="The username of the upload")
@option("--password", type=Str(), default=None, help="The password for the upload")
@option(
    "--publish-url", type=Str(), default=None, help="The URL of the upload endpoint"
)
@option(
    "--trusted-publishing",
    is_flag=True,
    default=False,
    help="Configure trusted publishing",
)
@option(
    "--native-tls",
    is_flag=True,
    default=False,
    help="Whether to load TLS certificates from the platform's native certificate store",
)
def publish_package_sub_cmd(
    *,
    username: str | None = None,
    password: SecretLike | None = None,
    publish_url: str | None = None,
    trusted_publishing: bool = False,
    native_tls: bool = False,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    publish_package(
        username=username,
        password=password,
        publish_url=publish_url,
        trusted_publishing=trusted_publishing,
        native_tls=native_tls,
    )


__all__ = ["publish_package_sub_cmd"]
