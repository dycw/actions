from __future__ import annotations

from click import group
from utilities.click import CONTEXT_SETTINGS

from actions import __version__
from actions.clean_dir.cli import clean_dir_sub_cmd
from actions.clean_dir.constants import CLEAN_DIR_DOCSTRING, CLEAN_DIR_SUB_CMD
from actions.git_clone_with.cli import git_clone_with_sub_cmd
from actions.git_clone_with.constants import (
    GIT_CLONE_WITH_DOCSTRING,
    GIT_CLONE_WITH_SUB_CMD,
)
from actions.pre_commit.conformalize_repo.cli import conformalize_repo_sub_cmd
from actions.pre_commit.conformalize_repo.constants import (
    CONFORMALIZE_REPO_DOCSTRING,
    CONFORMALIZE_REPO_SUB_CMD,
)
from actions.pre_commit.format_requirements.cli import format_requirements_sub_cmd
from actions.pre_commit.format_requirements.constants import (
    FORMAT_REQUIREMENTS_DOCSTRING,
    FORMAT_REQUIREMENTS_SUB_CMD,
)
from actions.pre_commit.replace_sequence_strs.cli import replace_sequence_strs_sub_cmd
from actions.pre_commit.replace_sequence_strs.constants import (
    REPLACE_SEQUENCE_STRS_DOCSTRING,
    REPLACE_SEQUENCE_STRS_SUB_CMD,
)
from actions.pre_commit.touch_empty_py.cli import touch_empty_py_sub_cmd
from actions.pre_commit.touch_empty_py.constants import (
    TOUCH_EMPTY_PY_DOCSTRING,
    TOUCH_EMPTY_PY_SUB_CMD,
)
from actions.pre_commit.touch_py_typed.cli import touch_py_typed_sub_cmd
from actions.pre_commit.touch_py_typed.constants import (
    TOUCH_PY_TYPED_DOCSTRING,
    TOUCH_PY_TYPED_SUB_CMD,
)
from actions.pre_commit.update_requirements.cli import update_requirements_sub_cmd
from actions.pre_commit.update_requirements.constants import (
    UPDATE_REQUIREMENTS_DOCSTRING,
    UPDATE_REQUIREMENTS_SUB_CMD,
)
from actions.publish_package.cli import publish_package_sub_cmd
from actions.publish_package.constants import (
    PUBLISH_PACKAGE_DOCSTRING,
    PUBLISH_PACKAGE_SUB_CMD,
)
from actions.random_sleep.cli import random_sleep_sub_cmd
from actions.random_sleep.constants import RANDOM_SLEEP_DOCSTRING, RANDOM_SLEEP_SUB_CMD
from actions.re_encrypt.cli import re_encrypt_sub_cmd
from actions.re_encrypt.constants import RE_ENCRYPT_DOCSTRING, RE_ENCRYPT_SUB_CMD
from actions.register_gitea_runner.cli import register_gitea_runner_sub_cmd
from actions.register_gitea_runner.constants import (
    REGISTER_GITEA_RUNNER_DOCSTRING,
    REGISTER_GITEA_RUNNER_SUB_CMD,
)
from actions.run_hooks.cli import run_hooks_sub_cmd
from actions.run_hooks.constants import RUN_HOOKS_DOCSTRING, RUN_HOOKS_SUB_CMD
from actions.setup_cronjob.cli import setup_cronjob_sub_cmd
from actions.setup_cronjob.constants import (
    SETUP_CRONJOB_DOCSTRING,
    SETUP_CRONJOB_SUB_CMD,
)
from actions.setup_ssh_config.cli import setup_ssh_config_sub_cmd
from actions.setup_ssh_config.constants import (
    SETUP_SSH_CONFIG_DOCSTRING,
    SETUP_SSH_CONFIG_SUB_CMD,
)
from actions.tag_commit.cli import tag_commit_sub_cmd
from actions.tag_commit.constants import TAG_COMMIT_DOCSTRING, TAG_COMMIT_SUB_CMD


@group(help=f"'actions' {__version__}", **CONTEXT_SETTINGS)
def _main() -> None: ...


_ = _main.command(name=CLEAN_DIR_SUB_CMD, help=CLEAN_DIR_DOCSTRING, **CONTEXT_SETTINGS)(
    clean_dir_sub_cmd
)
_ = _main.command(
    name=GIT_CLONE_WITH_SUB_CMD, help=GIT_CLONE_WITH_DOCSTRING, **CONTEXT_SETTINGS
)(git_clone_with_sub_cmd)
_ = _main.command(
    name=PUBLISH_PACKAGE_SUB_CMD, help=PUBLISH_PACKAGE_DOCSTRING, **CONTEXT_SETTINGS
)(publish_package_sub_cmd)
_ = _main.command(name=RUN_HOOKS_SUB_CMD, help=RUN_HOOKS_DOCSTRING, **CONTEXT_SETTINGS)(
    run_hooks_sub_cmd
)
_ = _main.command(
    name=RANDOM_SLEEP_SUB_CMD, help=RANDOM_SLEEP_DOCSTRING, **CONTEXT_SETTINGS
)(random_sleep_sub_cmd)
_ = _main.command(
    name=RE_ENCRYPT_SUB_CMD, help=RE_ENCRYPT_DOCSTRING, **CONTEXT_SETTINGS
)(re_encrypt_sub_cmd)
_ = _main.command(
    name=REGISTER_GITEA_RUNNER_SUB_CMD,
    help=REGISTER_GITEA_RUNNER_DOCSTRING,
    **CONTEXT_SETTINGS,
)(register_gitea_runner_sub_cmd)
_ = _main.command(
    name=SETUP_CRONJOB_SUB_CMD, help=SETUP_CRONJOB_DOCSTRING, **CONTEXT_SETTINGS
)(setup_cronjob_sub_cmd)
_ = _main.command(
    name=SETUP_SSH_CONFIG_SUB_CMD, help=SETUP_SSH_CONFIG_DOCSTRING, **CONTEXT_SETTINGS
)(setup_ssh_config_sub_cmd)
_ = _main.command(
    name=TAG_COMMIT_SUB_CMD, help=TAG_COMMIT_DOCSTRING, **CONTEXT_SETTINGS
)(tag_commit_sub_cmd)


@_main.group(name="pre-commit", help="Pre-commit hooks", **CONTEXT_SETTINGS)
def pre_commit_sub_cmd() -> None: ...


_ = pre_commit_sub_cmd.command(
    name=CONFORMALIZE_REPO_SUB_CMD, help=CONFORMALIZE_REPO_DOCSTRING, **CONTEXT_SETTINGS
)(conformalize_repo_sub_cmd)
_ = pre_commit_sub_cmd.command(
    name=FORMAT_REQUIREMENTS_SUB_CMD,
    help=FORMAT_REQUIREMENTS_DOCSTRING,
    **CONTEXT_SETTINGS,
)(format_requirements_sub_cmd)
_ = pre_commit_sub_cmd.command(
    name=REPLACE_SEQUENCE_STRS_SUB_CMD,
    help=REPLACE_SEQUENCE_STRS_DOCSTRING,
    **CONTEXT_SETTINGS,
)(replace_sequence_strs_sub_cmd)
_ = pre_commit_sub_cmd.command(
    name=TOUCH_EMPTY_PY_SUB_CMD, help=TOUCH_EMPTY_PY_DOCSTRING, **CONTEXT_SETTINGS
)(touch_empty_py_sub_cmd)
_ = pre_commit_sub_cmd.command(
    name=TOUCH_PY_TYPED_SUB_CMD, help=TOUCH_PY_TYPED_DOCSTRING, **CONTEXT_SETTINGS
)(touch_py_typed_sub_cmd)
_ = pre_commit_sub_cmd.command(
    name=UPDATE_REQUIREMENTS_SUB_CMD,
    help=UPDATE_REQUIREMENTS_DOCSTRING,
    **CONTEXT_SETTINGS,
)(update_requirements_sub_cmd)

if __name__ == "__main__":
    _main()
