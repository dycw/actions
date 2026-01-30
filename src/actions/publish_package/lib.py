from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.core import TemporaryDirectory, to_logger

from actions.utilities import logged_run

if TYPE_CHECKING:
    from utilities.types import SecretLike


_LOGGER = to_logger(__name__)


def publish_package(
    *,
    username: str | None = None,
    password: SecretLike | None = None,
    publish_url: str | None = None,
    trusted_publishing: bool = False,
    native_tls: bool = False,
) -> None:
    _LOGGER.info("Publishing package...")
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
    _LOGGER.info("Finished publishing package")


__all__ = ["publish_package"]
