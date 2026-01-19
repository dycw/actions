from __future__ import annotations

from typed_settings import load_settings, option, settings

from actions.utilities import LOADER


@settings
class Settings:
    description: str | None = option(default=None, help="Repo description")
    package_name: str | None = option(default=None, help="Package name")
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

    @property
    def python_package_name_use(self) -> str | None:
        if self.python_package_name is not None:
            return self.python_package_name
        if self.package_name is not None:
            return self.package_name.replace("-", "_")
        return None


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["SETTINGS", "Settings"]
