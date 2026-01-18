from __future__ import annotations

from contextlib import suppress
from os import environ, getenv
from pathlib import Path

from typed_settings import load_settings, option, settings
from utilities.constants import CPU_COUNT, HOSTNAME, SYSTEM, USER

from actions.utilities import LOADER

_DEFAULT_HOST = "gitea.main"
_RUNNER_INSTANCE_NAME_PARTS: list[str] = [USER, HOSTNAME]
with suppress(KeyError):
    _RUNNER_INSTANCE_NAME_PARTS.append(environ["SUBNET"])
_RUNNER_INSTANCE_NAME = "--".join(_RUNNER_INSTANCE_NAME_PARTS).lower()


@settings
class Settings:
    ssh_user: str = option(default="nonroot", help="SSH username")
    ssh_host: str = option(default=_DEFAULT_HOST, help="SSH host")
    gitea_container_user: str = option(default="git", help="Gitea container user name")
    gitea_container_name: str = option(default="gitea", help="Gitea container name")
    runner_certificate: Path = option(
        default=Path("root.pem"), help="Runner root certificate"
    )
    runner_capacity: int = option(
        default=max(round(CPU_COUNT / 2), 1), help="Runner capacity"
    )
    runner_labels: list[str] = option(
        factory=lambda: [f"host-{SYSTEM}"], help="Runner labels"
    )
    runner_instance_name: str = option(
        default=_RUNNER_INSTANCE_NAME, help="Runner instance name"
    )
    gitea_host: str = option(default=_DEFAULT_HOST, help="Gitea host")
    gitea_port: int = option(default=3000, help="Gitea port")
    runner_container_name: str = option(default="runner", help="Runner container name")


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["SETTINGS", "Settings"]
