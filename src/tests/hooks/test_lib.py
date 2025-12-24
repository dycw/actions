from __future__ import annotations

from pytest import mark, param

from actions.hooks.lib import _yield_hooks


class TestYieldHooks:
    @mark.parametrize(
        ("repos", "expected"),
        [param([], []), param(["dycw/pre-commit-hook-nitpick"], ["nitpick"])],
    )
    def test_repos(self, *, repos: list[str], expected: list[str]) -> None:
        result = list(_yield_hooks(repos=repos))
        assert result == expected

    @mark.parametrize(
        ("hooks", "expected"),
        [
            param([], []),
            param(["invalid"], []),
            param(["nitpick"], ["nitpick"]),
            param(
                ["nitpick", "no-commit-to-branch"], ["nitpick", "no-commit-to-branch"]
            ),
        ],
    )
    def test_hooks(self, *, hooks: list[str], expected: list[str]) -> None:
        result = list(_yield_hooks(hooks=hooks))
        assert result == expected
