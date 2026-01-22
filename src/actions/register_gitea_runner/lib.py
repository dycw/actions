from __future__ import annotations

from pathlib import Path
from re import search
from string import Template
from typing import TYPE_CHECKING

from requests import get
from utilities.core import always_iterable, get_func_name, write_bytes, write_text
from utilities.subprocess import rm_cmd, ssh, sudo_cmd
from utilities.tabulate import func_param_desc

from actions import __version__
from actions.constants import YAML_INSTANCE
from actions.logging import LOGGER
from actions.register_gitea_runner.constants import (
    PATH_CACHE,
    PATH_CONFIGS,
    PATH_WAIT_FOR_IT,
    URL_WAIT_FOR_IT,
)
from actions.register_gitea_runner.settings import SETTINGS
from actions.utilities import logged_run, yaml_dump

if TYPE_CHECKING:
    from utilities.types import MaybeSequenceStr, PathLike, StrDict


def register_gitea_runner(
    *,
    runner_token: str = SETTINGS.runner_token,
    ssh_user: str = SETTINGS.ssh_user,
    ssh_host: str = SETTINGS.ssh_host,
    gitea_container_user: str = SETTINGS.gitea_container_user,
    gitea_container_name: str = SETTINGS.gitea_container_name,
    runner_certificate: PathLike = SETTINGS.runner_certificate,
    runner_capacity: int = SETTINGS.runner_capacity,
    runner_labels: MaybeSequenceStr | None = SETTINGS.runner_labels,
    runner_container_name: str = SETTINGS.runner_container_name,
    gitea_host: str = SETTINGS.gitea_host,
    gitea_port: int = SETTINGS.gitea_port,
    runner_instance_name: str = SETTINGS.runner_instance_name,
) -> None:
    """Register against a remote instance of Gitea."""
    LOGGER.info(
        func_param_desc(
            register_gitea_runner,
            __version__,
            f"{runner_token=}",
            f"{ssh_user=}",
            f"{ssh_host=}",
            f"{gitea_container_user=}",
            f"{gitea_container_name=}",
            f"{runner_certificate=}",
            f"{runner_capacity=}",
            f"{runner_labels=}",
            f"{runner_container_name=}",
            f"{gitea_host=}",
            f"{gitea_port=}",
            f"{runner_instance_name=}",
        )
    )
    if runner_token is None:
        runner_token_use = ssh(
            ssh_user,
            ssh_host,
            *_docker_exec_generate(
                user=gitea_container_user, name=gitea_container_name
            ),
            return_=True,
        )
        LOGGER.info("Got token %r", runner_token_use)
    else:
        runner_token_use = runner_token
    _start_runner(
        runner_token_use,
        runner_certificate=runner_certificate,
        runner_capacity=runner_capacity,
        runner_labels=runner_labels,
        runner_container_name=runner_container_name,
        gitea_host=gitea_host,
        gitea_port=gitea_port,
        runner_instance_name=runner_instance_name,
    )
    LOGGER.info("Finished running %r", get_func_name(register_gitea_runner))


def register_against_local(
    *,
    gitea_container_user: str = SETTINGS.gitea_container_user,
    gitea_container_name: str = SETTINGS.gitea_container_name,
    runner_certificate: PathLike = SETTINGS.runner_certificate,
    runner_capacity: int = SETTINGS.runner_capacity,
    runner_container_name: str = SETTINGS.runner_container_name,
    gitea_host: str = SETTINGS.gitea_host,
    gitea_port: int = SETTINGS.gitea_port,
    runner_instance_name: str = SETTINGS.runner_instance_name,
) -> None:
    """Register against a local instance of Gitea."""
    LOGGER.info("Registering against %s:%d...", gitea_host, gitea_port)
    token = logged_run(
        *_docker_exec_generate(user=gitea_container_user, name=gitea_container_name),
        return_=True,
    )
    _start_runner(
        token,
        runner_certificate=runner_certificate,
        runner_capacity=runner_capacity,
        runner_container_name=runner_container_name,
        gitea_host=gitea_host,
        gitea_port=gitea_port,
        runner_instance_name=runner_instance_name,
    )


def _check_certificate(*, certificate: PathLike = SETTINGS.runner_certificate) -> None:
    if not Path(certificate).is_file():
        msg = f"Missing certificate {str(certificate)!r}"
        raise FileNotFoundError(msg)


def _check_token(text: str, /) -> None:
    if not search(r"^[A-Za-z0-9]{40}$", text):
        msg = f"Invalid token; got {text!r}"
        raise ValueError(msg)


def _docker_exec_generate(
    *,
    user: str = SETTINGS.gitea_container_user,
    name: str = SETTINGS.gitea_container_name,
) -> list[str]:
    return [
        "docker",
        "exec",
        "--user",
        user,
        name,
        "gitea",
        "actions",
        "generate-runner-token",
    ]


def _docker_run_act_runner_args(
    token: str,
    /,
    *,
    host: str = SETTINGS.gitea_host,
    port: int = SETTINGS.gitea_port,
    runner_certificate: PathLike = SETTINGS.runner_certificate,
    instance_name: str = SETTINGS.runner_instance_name,
    container_name: str = SETTINGS.runner_container_name,
) -> list[str]:
    config_host = _get_config_path(token)
    config_cont = "/config.yml"
    entrypoint_host = _get_entrypoint_path(host=host, port=port)
    entrypoint_cont = Path("/usr/local/bin/entrypoint.sh")
    return [
        "docker",
        "run",
        "--detach",
        "--entrypoint",
        str(entrypoint_cont),
        "--env",
        f"CONFIG_FILE={config_cont}",
        "--env",
        f"GITEA_INSTANCE_URL=https://{host}:{port}",
        "--env",
        f"GITEA_RUNNER_NAME={instance_name}",
        "--env",
        f"GITEA_RUNNER_REGISTRATION_TOKEN={token}",
        "--name",
        container_name,
        "--restart",
        "always",
        "--volume",
        "/var/run/docker.sock:/var/run/docker.sock",
        "--volume",
        f"{PATH_WAIT_FOR_IT}:/usr/local/bin/wait-for-it.sh:ro",
        "--volume",
        f"{Path.cwd()}/data:/data",
        "--volume",
        f"{config_host}:{config_cont}:ro",
        "--volume",
        f"{entrypoint_host}:{entrypoint_cont}:ro",
        "--volume",
        f"{runner_certificate}:/etc/ssl/certs/runner-certificate.pem:ro",
        "gitea/act_runner",
    ]


def _docker_stop_runner_args(
    *, name: str = SETTINGS.runner_container_name
) -> list[str]:
    return ["docker", "rm", "--force", name]


def _get_config_contents(
    *,
    capacity: int = SETTINGS.runner_capacity,
    certificate: PathLike = SETTINGS.runner_certificate,
    labels: MaybeSequenceStr | None = SETTINGS.runner_labels,
) -> str:
    src = PATH_CONFIGS / "config.yml"
    text = Template(src.read_text()).safe_substitute(
        CAPACITY=capacity, CERTIFICATE=certificate
    )
    if labels is None:
        return text
    dict_ = YAML_INSTANCE.load(text)
    runner: StrDict = dict_["runner"]
    labels_list: list[str] = runner["labels"]
    labels_list.extend(always_iterable(labels))
    return yaml_dump(dict_)


def _get_config_path(token: str, /) -> Path:
    return PATH_CACHE / f"configs/{token}.yml"


def _get_entrypoint_contents(
    *, host: str = SETTINGS.gitea_host, port: int = SETTINGS.gitea_port
) -> str:
    src = PATH_CONFIGS / "entrypoint.sh"
    return Template(src.read_text()).safe_substitute(GITEA_HOST=host, GITEA_PORT=port)


def _get_entrypoint_path(
    *, host: str = SETTINGS.gitea_host, port: int = SETTINGS.gitea_port
) -> Path:
    return PATH_CACHE / f"entrypoints/{host}-{port}"


def _start_runner(
    token: str,
    /,
    *,
    runner_certificate: PathLike = SETTINGS.runner_certificate,
    runner_capacity: int = SETTINGS.runner_capacity,
    runner_labels: MaybeSequenceStr | None = SETTINGS.runner_labels,
    runner_container_name: str = SETTINGS.runner_container_name,
    gitea_host: str = SETTINGS.gitea_host,
    gitea_port: int = SETTINGS.gitea_port,
    runner_instance_name: str = SETTINGS.runner_instance_name,
) -> None:
    _check_certificate(certificate=runner_certificate)
    _check_token(token)
    _write_config(
        token,
        capacity=runner_capacity,
        certificate=runner_certificate,
        labels=runner_labels,
    )
    _write_entrypoint(host=gitea_host, port=gitea_port)
    _write_wait_for_it()
    logged_run(*_docker_stop_runner_args(name=runner_container_name))
    logged_run(*sudo_cmd(*rm_cmd("data")))
    logged_run(
        *_docker_run_act_runner_args(
            token,
            host=gitea_host,
            port=gitea_port,
            runner_certificate=runner_certificate,
            instance_name=runner_instance_name,
            container_name=runner_container_name,
        )
    )


def _write_config(
    token: str,
    /,
    *,
    capacity: int = SETTINGS.runner_capacity,
    certificate: PathLike = SETTINGS.runner_certificate,
    labels: MaybeSequenceStr | None = SETTINGS.runner_labels,
) -> None:
    dest = _get_config_path(token)
    text = _get_config_contents(
        capacity=capacity, certificate=certificate, labels=labels
    )
    write_text(dest, text, overwrite=True)


def _write_entrypoint(
    *, host: str = SETTINGS.gitea_host, port: int = SETTINGS.gitea_port
) -> None:
    dest = _get_entrypoint_path(host=host, port=port)
    text = _get_entrypoint_contents(host=host, port=port)
    write_text(dest, text, overwrite=True, perms="u=rwx,g=rx,o=rx")


def _write_wait_for_it() -> None:
    if PATH_WAIT_FOR_IT.is_file():
        return
    resp = get(URL_WAIT_FOR_IT, timeout=60)
    resp.raise_for_status()
    write_bytes(PATH_WAIT_FOR_IT, resp.content, overwrite=True, perms="u=rwx,g=rx,o=rx")


__all__ = ["register_against_local"]
