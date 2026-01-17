from __future__ import annotations

from pathlib import Path

from typed_settings import load_settings, option, settings
from utilities.constants import USER
from utilities.socket import HOSTNAME

from actions.utilities import LOADER


@settings
class Settings:
    ssh_user: str = option(default="user", help="SSH username")
    ssh_host: str = option(default="gitea", help="SSH host")
    gitea_container_user: str = option(default="git", help="Gitea container user name")
    gitea_container_name: str = option(default="gitea", help="Gitea container name")
    gitea_host: str = option(default="gitea", help="Gitea host")
    gitea_port: int = option(default=3000, help="Gitea port")
    runner_capacity: int = option(default=1, help="Runner capacity")
    runner_instance_name: str = option(
        default=f"{USER}--{HOSTNAME}", help="Runner instance name"
    )
    runner_certificate: Path = option(
        default=Path("root.pem"), help="Runner root certificate"
    )
    runner_container_name: str = option(default="runner", help="Runner container name")


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["SETTINGS", "Settings"]
