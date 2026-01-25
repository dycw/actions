from __future__ import annotations

from contextlib import suppress
from subprocess import CalledProcessError

from utilities.version import Version3

from actions.logging import LOGGER
from actions.tag_commit.constants import USER_EMAIL, USER_NAME
from actions.utilities import logged_run


def tag_commit(
    *,
    user_name: str = USER_NAME,
    user_email: str = USER_EMAIL,
    major_minor: bool = False,
    major: bool = False,
    latest: bool = False,
) -> None:
    LOGGER.info("Tagging commit...")
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
    LOGGER.info("Finished tagging commit")


def _tag(version: str, /) -> None:
    with suppress(CalledProcessError):
        logged_run("git", "tag", "--delete", version)
    with suppress(CalledProcessError):
        logged_run("git", "push", "--delete", "origin", version)
    logged_run("git", "tag", "-a", version, "HEAD", "-m", version)
    logged_run("git", "push", "--tags", "--force", "--set-upstream", "origin")


__all__ = ["tag_commit"]
