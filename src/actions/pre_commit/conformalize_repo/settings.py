from __future__ import annotations

from typed_settings import Secret, load_settings, option, secret, settings

from actions.utilities import LOADER


@settings
class Settings:
    ci__certificates: bool = option(
        default=False, help="Update CA certficates before each step"
    )
    ci__gitea: bool = option(default=False, help="Set up CI on Gitea")
    ci__token_checkout: Secret[str] | None = secret(
        default=None, help="Set up CI with this checkout token"
    )
    ci__token_github: Secret[str] | None = secret(
        default=None, help="Set up CI with this GitHub token"
    )
    ci__pull_request__pre_commit: bool = option(
        default=False, help="Set up CI 'pull-request.yaml' pre-commit"
    )
    ci__pull_request__pre_commit__submodules: str | None = option(
        default=None, help="Set up CI 'pull-request.yaml' pre-commit with submodules"
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
    ci__pull_request__pytest__all_versions: bool = option(
        default=False, help="Set up CI 'pull-request.yaml' pytest with all versions"
    )
    ci__pull_request__pytest__sops_age_key: Secret[str] | None = secret(
        default=None,
        help="Set up CI 'pull-request.yaml' pytest with this 'age' key for 'sops'",
    )
    ci__pull_request__ruff: bool = option(
        default=False, help="Set up CI 'pull-request.yaml' ruff"
    )
    ci__push__publish__github: bool = option(
        default=False, help="Set up CI 'push.yaml' publishing to GitHub"
    )
    ci__push__publish__primary: bool = option(
        default=False, help="Set up CI 'push.yaml' publishing #1"
    )
    ci__push__publish__primary__job_name: str = option(
        default="pypi", help="Set up CI 'push.yaml' publishing #1 with this job name"
    )
    ci__push__publish__primary__username: str | None = option(
        default=None, help="Set up CI 'push.yaml' publishing #1 with this username"
    )
    ci__push__publish__primary__password: Secret[str] | None = secret(
        default=None, help="Set up CI 'push.yaml' publishing #1 with this password"
    )
    ci__push__publish__primary__publish_url: str | None = option(
        default=None, help="Set up CI 'push.yaml' publishing #1 with this URL"
    )
    ci__push__publish__secondary: bool = option(
        default=False, help="Set up CI 'push.yaml' publishing #2"
    )
    ci__push__publish__secondary__job_name: str = option(
        default="pypi2", help="Set up CI 'push.yaml' publishing #2 with this job name"
    )
    ci__push__publish__secondary__username: str | None = option(
        default=None, help="Set up CI 'push.yaml' publishing #2 with this username"
    )
    ci__push__publish__secondary__password: Secret[str] | None = secret(
        default=None, help="Set up CI 'push.yaml' publishing #2 with this password"
    )
    ci__push__publish__secondary__publish_url: str | None = option(
        default=None, help="Set up CI 'push.yaml' publishing #2 with this URL"
    )
    ci__push__tag: bool = option(default=False, help="Set up CI 'push.yaml' tagging")
    ci__push__tag__all: bool = option(
        default=False, help="Set up CI 'push.yaml' tagging with all tags"
    )
    coverage: bool = option(default=False, help="Set up '.coveragerc.toml'")
    description: str | None = option(default=None, help="Repo description")
    envrc: bool = option(default=False, help="Set up '.envrc'")
    envrc__uv: bool = option(default=False, help="Set up '.envrc' with uv")
    package_name: str | None = option(default=None, help="Package name")
    pyproject: bool = option(default=False, help="Set up 'pyproject.toml'")
    pyproject__project__optional_dependencies__scripts: bool = option(
        default=False,
        help="Set up 'pyproject.toml' [project.optional-dependencies.scripts]",
    )
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
    uv__indexes: list[tuple[str, str]] = option(
        factory=list, help="Set up 'uv' with index indexes"
    )
    uv__native_tls: bool = option(default=False, help="Setup 'uv' with native TLS")
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
