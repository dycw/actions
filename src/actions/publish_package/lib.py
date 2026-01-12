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
    with TemporaryDirectory() as temp:
        logged_run("uv", "build", "--out-dir", str(temp), "--wheel", "--clear")
        logged_run(
            "uv",
            "publish",
            *([] if username is None else ["--username", username]),
            *([] if password is None else ["--password", password]),
            *([] if publish_url is None else ["--publish-url", publish_url]),
            *(["--trusted-publishing", "always"] if trusted_publishing else []),
            *(["--native-tls"] if native_tls else []),
            f"{temp}/*",
        )
    LOGGER.info("Finished running %r", get_func_name(publish_package))


__all__ = ["publish_package"]
