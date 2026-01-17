from __future__ import annotations

from utilities.constants import USER

from actions.setup_cronjob.lib import _get_crontab


class TestGetCronTab:
    def test_main(self) -> None:
        result = _get_crontab()
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s true; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | sudo tee -a /var/log/name.log
"""
        assert result == expected

    def test_prepend_path(self) -> None:
        result = _get_crontab(prepend_path=["/foo/bin"])
        expected = f"""\
PATH=/foo/bin:/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s true; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | sudo tee -a /var/log/name.log
"""
        assert result == expected

    def test_schedule(self) -> None:
        result = _get_crontab(schedule="*/5 * * * *")
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

*/5 * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s true; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | sudo tee -a /var/log/name.log
"""
        assert result == expected

    def test_user(self) -> None:
        result = _get_crontab(user="user")
        expected = """\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * user (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s true; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | sudo tee -a /var/log/name.log
"""
        assert result == expected

    def test_timeout(self) -> None:
        result = _get_crontab(timeout=120)
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 120s true; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | sudo tee -a /var/log/name.log
"""
        assert result == expected

    def test_kill_after(self) -> None:
        result = _get_crontab(kill_after=20)
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=20s --verbose 60s true; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | sudo tee -a /var/log/name.log
"""
        assert result == expected

    def test_command(self) -> None:
        result = _get_crontab(command="other-cmd")
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s other-cmd; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | sudo tee -a /var/log/name.log
"""
        assert result == expected

    def test_args(self) -> None:
        result = _get_crontab(args=["--dry-run"])
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s true --dry-run; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | sudo tee -a /var/log/name.log
"""
        assert result == expected
