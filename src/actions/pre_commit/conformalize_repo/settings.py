from __future__ import annotations

from typed_settings import load_settings, option, settings

from actions.pre_commit.conformalize_repo.constants import RUN_VERSION_BUMP
from actions.utilities import LOADER


@settings
class Settings:
    ci__gitea: bool = option(default=False, help="Set up CI on Gitea")
    ci__pull_request__pre_commit: bool = option(
        default=False, help="Set up CI 'pull-request.yaml' pre-commit"
    )
    ci__pull_request__pyright: bool = option(
        default=False, help="Set up CI 'pull-request.yaml' pyright"
    )
    ci__pull_request__pytest__macos: bool = option(
        default=False, help="Set up CI 'pull-request.yaml' pytest with MacOS"
    )
    ci__pull_request__pytest__ubuntu: bool = option(
        default=False, help="Set up CI 'pull-request.yaml' pytest with Ubuntu"
    )
    ci__pull_request__pytest__windows: bool = option(
        default=False, help="Set up CI 'pull-request.yaml' pytest with Windows"
    )
    ci__pull_request__ruff: bool = option(
        default=False, help="Set up CI 'pull-request.yaml' ruff"
    )
    ci__push__publish: bool = option(
        default=False, help="Set up CI 'push.yaml' publishing"
    )
    ci__push__tag: bool = option(default=False, help="Set up CI 'push.yaml' tagging")
    coverage: bool = option(default=False, help="Set up '.coveragerc.toml'")
    description: str | None = option(default=None, help="Repo description")
    envrc: bool = option(default=False, help="Set up '.envrc'")
    envrc__uv: bool = option(default=False, help="Set up '.envrc' with uv")
    envrc__uv__native_tls: bool = option(
        default=False, help="Set up '.envrc' with uv native TLS"
    )
    gitignore: bool = option(default=False, help="Set up '.gitignore'")
    package_name: str | None = option(default=None, help="Package name")
    pre_commit__dockerfmt: bool = option(
        default=False, help="Set up '.pre-commit-config.yaml' dockerfmt"
    )
    pre_commit__prettier: bool = option(
        default=False, help="Set up '.pre-commit-config.yaml' prettier"
    )
    pre_commit__python: bool = option(
        default=False, help="Set up '.pre-commit-config.yaml' python"
    )
    pre_commit__ruff: bool = option(
        default=False, help="Set up '.pre-commit-config.yaml' ruff"
    )
    pre_commit__shell: bool = option(
        default=False, help="Set up '.pre-commit-config.yaml' shell"
    )
    pre_commit__taplo: bool = option(
        default=False, help="Set up '.pre-commit-config.yaml' taplo"
    )
    pre_commit__uv: bool = option(
        default=False, help="Set up '.pre-commit-config.yaml' uv"
    )
    pre_commit__uv__script: str | None = option(
        default=None, help="Set up '.pre-commit-config.yaml' uv lock script"
    )
    pyproject: bool = option(default=False, help="Set up 'pyproject.toml'")
    pyproject__project__optional_dependencies__scripts: bool = option(
        default=False,
        help="Set up 'pyproject.toml' [project.optional-dependencies.scripts]",
    )
    pyproject__tool__uv__indexes: list[tuple[str, str]] = option(
        factory=list, help="Set up 'pyproject.toml' [[uv.tool.index]]"
    )
    pyright: bool = option(default=False, help="Set up 'pyrightconfig.json'")
    pytest: bool = option(default=False, help="Set up 'pytest.toml'")
    pytest__asyncio: bool = option(default=False, help="Set up 'pytest.toml' asyncio_*")
    pytest__ignore_warnings: bool = option(
        default=False, help="Set up 'pytest.toml' filterwarnings"
    )
    pytest__timeout: int | None = option(
        default=None, help="Set up 'pytest.toml' timeout"
    )
    python_package_name: str | None = option(
        default=None, help="Python package name override"
    )
    python_version: str = option(default="3.14", help="Python version")
    readme: bool = option(default=False, help="Set up 'README.md'")
    repo_name: str | None = option(default=None, help="Repo name")
    ruff: bool = option(default=False, help="Set up 'ruff.toml'")
    run_version_bump: bool = option(default=RUN_VERSION_BUMP, help="Run version bump")
    script: str | None = option(
        default=None, help="Set up a script instead of a package"
    )

    @property
    def python_package_name_use(self) -> str | None:
        if self.python_package_name is not None:
            return self.python_package_name
        if self.package_name is not None:
            return self.package_name.replace("-", "_")
        return None


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["SETTINGS", "Settings"]
