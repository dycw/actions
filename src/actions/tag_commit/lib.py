from __future__ import annotations

from contextlib import suppress
from subprocess import CalledProcessError

from utilities.functions import get_func_name
from utilities.tabulate import func_param_desc
from utilities.version import Version3

from actions import __version__
from actions.logging import LOGGER
from actions.tag_commit.settings import SETTINGS
from actions.utilities import logged_run


def tag_commit(
    *,
    user_name: str = SETTINGS.user_name,
    user_email: str = SETTINGS.user_email,
    major_minor: bool = SETTINGS.major_minor,
    major: bool = SETTINGS.major,
    latest: bool = SETTINGS.latest,
) -> None:
    LOGGER.info(
        func_param_desc(
            tag_commit,
            __version__,
            f"{user_name=}",
            f"{user_email=}",
            f"{major_minor=}",
            f"{major=}",
            f"{latest=}",
        )
    )
    logged_run("git", "config", "--global", "user.name", user_name)
    logged_run("git", "config", "--global", "user.email", user_email)
    version = Version3.parse(
        logged_run("bump-my-version", "show", "current_version", return_=True)
    )
    _tag(str(version))
    if major_minor:
        _tag(f"{version.major}.{version.minor}")
    if major:
        _tag(str(version.major))
    if latest:
        _tag("latest")
    LOGGER.info("Finished running %r", get_func_name(tag_commit))


def _tag(version: str, /) -> None:
    with suppress(CalledProcessError):
        logged_run("git", "tag", "--delete", version)
    with suppress(CalledProcessError):
        logged_run("git", "push", "--delete", "origin", version)
    logged_run("git", "tag", "-a", version, "HEAD", "-m", version)
    logged_run("git", "push", "--tags", "--force", "--set-upstream", "origin")


__all__ = ["tag_commit"]
