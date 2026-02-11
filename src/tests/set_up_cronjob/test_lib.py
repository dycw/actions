from __future__ import annotations

from utilities.constants import USER

from actions.set_up_cronjob.lib import _get_crontab


class TestGetCronTab:
    def test_main(self) -> None:
        result = _get_crontab("name", "command")
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_prepend_path(self) -> None:
        result = _get_crontab("name", "command", prepend_path=["/foo/bin"])
        expected = f"""\
PATH=/foo/bin:/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_env_vars_one(self) -> None:
        result = _get_crontab("name", "command", env_vars={"KEY": "value"})
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin
KEY=value

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_env_vars_multiple(self) -> None:
        result = _get_crontab(
            "name", "command", env_vars={"KEY1": "value1", "KEY2": "value2"}
        )
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin
KEY1=value1
KEY2=value2

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_schedule(self) -> None:
        result = _get_crontab("name", "command", schedule="*/5 * * * *")
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

*/5 * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_user(self) -> None:
        result = _get_crontab("name", "command", user="user")
        expected = """\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * user (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_timeout(self) -> None:
        result = _get_crontab("name", "command", timeout=120)
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 120s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_kill_after(self) -> None:
        result = _get_crontab("name", "command", kill_after=20)
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=20s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_sudo(self) -> None:
        result = _get_crontab("name", "command", sudo=True)
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | sudo tee -a /var/log/name.log
"""
        assert result == expected

    def test_args(self) -> None:
        result = _get_crontab("name", "command", "--dry-run")
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command --dry-run; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected
