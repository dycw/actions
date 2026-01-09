from __future__ import annotations

from pytest import mark, param

from actions.constants import ACTIONS_URL
from actions.pre_commit.conformalize_repo.constants import CONFORMALIZE_REPO_SUB_CMD
from actions.pre_commit.format_requirements.constants import FORMAT_REQUIREMENTS_SUB_CMD
from actions.pre_commit.replace_sequence_strs.constants import (
    REPLACE_SEQUENCE_STRS_SUB_CMD,
)
from actions.pre_commit.touch_empty_py.constants import TOUCH_EMPTY_PY_SUB_CMD
from actions.pre_commit.touch_py_typed.constants import TOUCH_PY_TYPED_SUB_CMD
from actions.pre_commit.update_requirements.constants import UPDATE_REQUIREMENTS_SUB_CMD
from actions.run_hooks.lib import _yield_hooks


class TestYieldHooks:
    @mark.parametrize(
        ("repos", "expected"),
        [
            param([], []),
            param(
                [ACTIONS_URL],
                [
                    CONFORMALIZE_REPO_SUB_CMD,
                    FORMAT_REQUIREMENTS_SUB_CMD,
                    REPLACE_SEQUENCE_STRS_SUB_CMD,
                    TOUCH_EMPTY_PY_SUB_CMD,
                    TOUCH_PY_TYPED_SUB_CMD,
                    UPDATE_REQUIREMENTS_SUB_CMD,
                ],
            ),
        ],
    )
    def test_repos(self, *, repos: list[str], expected: list[str]) -> None:
        result = list(_yield_hooks(repos=repos))
        assert result == expected

    @mark.parametrize(
        ("hooks", "expected"),
        [
            param([], []),
            param(["invalid"], []),
            param([CONFORMALIZE_REPO_SUB_CMD], [CONFORMALIZE_REPO_SUB_CMD]),
            param(
                [CONFORMALIZE_REPO_SUB_CMD, "no-commit-to-branch"],
                [CONFORMALIZE_REPO_SUB_CMD, "no-commit-to-branch"],
            ),
        ],
    )
    def test_hooks(self, *, hooks: list[str], expected: list[str]) -> None:
        result = list(_yield_hooks(hooks=hooks))
        assert result == expected

    def test_hooks_exclude(self) -> None:
        result = list(
            _yield_hooks(repos=[ACTIONS_URL], hooks_exclude=[CONFORMALIZE_REPO_SUB_CMD])
        )
        expected = [
            FORMAT_REQUIREMENTS_SUB_CMD,
            REPLACE_SEQUENCE_STRS_SUB_CMD,
            TOUCH_EMPTY_PY_SUB_CMD,
            TOUCH_PY_TYPED_SUB_CMD,
            UPDATE_REQUIREMENTS_SUB_CMD,
        ]
        assert result == expected
