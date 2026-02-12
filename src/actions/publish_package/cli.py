from __future__ import annotations

from typing import TYPE_CHECKING

from click import Command, command, option
from utilities.click import CONTEXT_SETTINGS, SecretStr, Str
from utilities.core import is_pytest, set_up_logging

from actions.publish_package.lib import publish_package

if TYPE_CHECKING:
    from collections.abc import Callable

    from utilities.types import SecretLike


PUBLISH_PACKAGE_SUB_CMD = "publish-package"


def make_publish_package_cmd(
    *, cli: Callable[..., Command] = command, name: str | None = None
) -> Command:
    @option("--username", type=Str(), default=None, help="The username of the upload")
    @option(
        "--password", type=SecretStr(), default=None, help="The password for the upload"
    )
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
    def func(
        *,
        username: str | None = None,
        password: SecretLike | None = None,
        publish_url: str | None = None,
        trusted_publishing: bool = False,
        native_tls: bool = False,
    ) -> None:
        if is_pytest():
            return
        set_up_logging(__name__, root=True)
        publish_package(
            username=username,
            password=password,
            publish_url=publish_url,
            trusted_publishing=trusted_publishing,
            native_tls=native_tls,
        )

    return cli(name=name, help="Build and publish the package", **CONTEXT_SETTINGS)(
        func
    )


cli = make_publish_package_cmd()


__all__ = ["PUBLISH_PACKAGE_SUB_CMD", "cli", "make_publish_package_cmd"]
