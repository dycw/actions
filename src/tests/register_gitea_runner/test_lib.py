from __future__ import annotations

from actions.register_gitea_runner.lib import (
    _get_config_contents,
    _get_entrypoint_contents,
)


class TestGetConfigContents:
    def test_main(self) -> None:
        _ = _get_config_contents()


class TestGetEntrypointContents:
    def test_main(self) -> None:
        _ = _get_entrypoint_contents()
