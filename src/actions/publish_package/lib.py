from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.functions import get_func_name
from utilities.tabulate import func_param_desc
from utilities.tempfile import TemporaryDirectory

from actions import __version__
from actions.logging import LOGGER
from actions.publish_package.settings import SETTINGS
from actions.utilities import logged_run

if TYPE_CHECKING:
    from typed_settings import Secret

    from actions.types import SecretLike


def publish_package(
    *,
    username: str | None = SETTINGS.username,
    password: Secret[str] | None = SETTINGS.password,
    publish_url: str | None = SETTINGS.publish_url,
    trusted_publishing: bool = SETTINGS.trusted_publishing,
    native_tls: bool = SETTINGS.native_tls,
) -> None:
    LOGGER.info(
        func_param_desc(
            publish_package,
            __version__,
            f"{username=}",
            f"{password=}",
            f"{publish_url=}",
            f"{trusted_publishing=}",
            f"{native_tls=}",
        )
    )
    build_head: list[str] = ["uv", "build", "--out-dir"]
    build_tail: list[str] = ["--wheel", "--clear"]
    publish: list[SecretLike] = ["uv", "publish"]
    if username is not None:
        publish.extend(["--username", username])
    if password is not None:
        publish.extend(["--password", password])
    if publish_url is not None:
        publish.extend(["--publish-url", publish_url])
    if trusted_publishing:
        publish.extend(["--trusted-publishing", "always"])
    if native_tls:
        publish.append("--native-tls")
    with TemporaryDirectory() as temp:
        logged_run(*build_head, str(temp), *build_tail)
        logged_run(*publish, f"{temp}/*")
    LOGGER.info("Finished running %r", get_func_name(publish_package))


__all__ = ["publish_package"]
