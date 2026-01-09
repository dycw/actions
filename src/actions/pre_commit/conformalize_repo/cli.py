from __future__ import annotations

from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest

from actions.logging import LOGGER
from actions.pre_commit.conformalize_repo.lib import conformalize_repo
from actions.pre_commit.conformalize_repo.settings import Settings
from actions.utilities import LOADER


@click_options(Settings, [LOADER], show_envvars_in_help=True)
def conformalize_repo_sub_cmd(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    conformalize_repo(
        ci__ca_certificates=settings.ci__ca_certificates,
        ci__gitea=settings.ci__gitea,
        ci__token=settings.ci__token,
        ci__pull_request__pre_commit=settings.ci__pull_request__pre_commit,
        ci__pull_request__pyright=settings.ci__pull_request__pyright,
        ci__pull_request__pytest__macos=settings.ci__pull_request__pytest__macos,
        ci__pull_request__pytest__ubuntu=settings.ci__pull_request__pytest__ubuntu,
        ci__pull_request__pytest__windows=settings.ci__pull_request__pytest__windows,
        ci__pull_request__pytest__all_versions=settings.ci__pull_request__pytest__all_versions,
        ci__pull_request__pytest__sops_age_key=settings.ci__pull_request__pytest__sops_age_key,
        ci__pull_request__ruff=settings.ci__pull_request__ruff,
        ci__push__publish=settings.ci__push__publish,
        ci__push__tag=settings.ci__push__tag,
        ci__push__tag__all=settings.ci__push__tag__all,
        coverage=settings.coverage,
        description=settings.description,
        envrc=settings.envrc,
        envrc__uv=settings.envrc__uv,
        gitignore=settings.gitignore,
        package_name=settings.package_name,
        pre_commit__dockerfmt=settings.pre_commit__dockerfmt,
        pre_commit__prettier=settings.pre_commit__prettier,
        pre_commit__python=settings.pre_commit__python,
        pre_commit__ruff=settings.pre_commit__ruff,
        pre_commit__shell=settings.pre_commit__shell,
        pre_commit__taplo=settings.pre_commit__taplo,
        pre_commit__uv=settings.pre_commit__uv,
        pyproject=settings.pyproject,
        pyproject__project__optional_dependencies__scripts=settings.pyproject__project__optional_dependencies__scripts,
        pyproject__tool__uv__indexes=settings.pyproject__tool__uv__indexes,
        pyright=settings.pyright,
        pytest=settings.pytest,
        pytest__asyncio=settings.pytest__asyncio,
        pytest__ignore_warnings=settings.pytest__ignore_warnings,
        pytest__timeout=settings.pytest__timeout,
        python_package_name=settings.python_package_name,
        python_version=settings.python_version,
        readme=settings.readme,
        repo_name=settings.repo_name,
        ruff=settings.ruff,
        run_version_bump=settings.run_version_bump,
        script=settings.script,
        uv__native_tls=settings.uv__native_tls,
    )


__all__ = ["conformalize_repo_sub_cmd"]
