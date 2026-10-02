"""Commit and push a few paths to main, one process at a time (a file lock keeps daemons from colliding on git)."""
import fcntl
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / ".git" / "team_gitsync.lock"


def push(paths, message):
    git = ["git", "-C", str(ROOT)]
    with open(LOCK, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        subprocess.run(git + ["add", "--"] + paths, capture_output=True)
        if subprocess.run(git + ["diff", "--cached", "--quiet", "--"] + paths).returncode == 0:
            return
        subprocess.run(git + ["commit", "-q", "-m", message, "--"] + paths, capture_output=True)
        subprocess.run(git + ["pull", "--rebase", "--autostash", "-q"], capture_output=True)
        subprocess.run(git + ["push", "-q", "origin", "HEAD:main"], capture_output=True)
