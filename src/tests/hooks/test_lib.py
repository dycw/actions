from __future__ import annotations

from pytest import mark, param

from actions.run_hooks.lib import _yield_hooks


class TestYieldHooks:
    @mark.parametrize(
        ("repos", "expected"),
        [param([], []), param(["dycw/conformalize"], ["conformalize"])],
    )
    def test_repos(self, *, repos: list[str], expected: list[str]) -> None:
        result = list(_yield_hooks(repos=repos))
        assert result == expected

    @mark.parametrize(
        ("hooks", "expected"),
        [
            param([], []),
            param(["invalid"], []),
            param(["conformalize"], ["conformalize"]),
            param(
                ["conformalize", "no-commit-to-branch"],
                ["conformalize", "no-commit-to-branch"],
            ),
        ],
    )
    def test_hooks(self, *, hooks: list[str], expected: list[str]) -> None:
        result = list(_yield_hooks(hooks=hooks))
        assert result == expected
