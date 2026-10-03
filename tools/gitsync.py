"""Commit and push a few paths to main, one process at a time (a file lock keeps daemons from colliding on git).

It never pulls over work in progress (Sat 09:44-09:46: `pull --autostash` stashed a half-done code edit, the pull
conflicted with Aleks's push of the same files, and the rebase was left stuck, so every session's pull failed):
- a merge or rebase already under way: nothing is done;
- a tracked code edit in the tree (CODE): the commit stays local, no pull, no push;
- a pull that conflicts is aborted, never left half-done.
Each skip prints one line on stderr (the daemon's log). Nothing at all while run/git-paused exists."""
import fcntl
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE = ("agents/", "tools/", "tests/", "engine/", "broker/", "dashboard/", "hub/", "bazaar-kit/", "pyproject.toml",
        "uv.lock")                       # a teammate's push can conflict with an edit here (same as team_sync.sh)


def _run(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def busy(root=ROOT):
    """Why a pull must wait, or None."""
    gitdir = Path(_run(root, "rev-parse", "--absolute-git-dir").stdout.strip())
    for d in ("rebase-merge", "rebase-apply", "MERGE_HEAD"):
        if (gitdir / d).exists():
            return f"a {d} is under way"
    wip = [line[3:] for line in _run(root, "status", "--porcelain").stdout.splitlines()   # untracked files: a
           if not line.startswith("??") and line[3:].strip('"').startswith(CODE)]       # pull never stashes them
    return f"work in progress in {', '.join(wip[:3])}" if wip else None


def push(paths, message, root=ROOT):
    if (Path(root) / "run" / "git-paused").exists():
        return
    gitdir = Path(_run(root, "rev-parse", "--absolute-git-dir").stdout.strip())
    with open(gitdir / "team_gitsync.lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if (why := busy(root)) and "under way" in why:
            print(f"gitsync: {why}: nothing committed ({message})", file=sys.stderr, flush=True)
            return
        _run(root, "add", "--", *paths)
        if _run(root, "diff", "--cached", "--quiet", "--", *paths).returncode == 0:
            return
        _run(root, "commit", "-q", "-m", message, "--", *paths)
        if why:
            print(f"gitsync: {why}: committed, not pulled or pushed ({message})", file=sys.stderr, flush=True)
            return
        if _run(root, "pull", "--rebase", "--autostash", "-q", "origin", "main").returncode != 0:
            _run(root, "rebase", "--abort")
            print(f"gitsync: pull conflicted, aborted; committed, not pushed ({message})", file=sys.stderr, flush=True)
            return
        if _run(root, "push", "-q", "origin", "HEAD:main").returncode != 0:
            print(f"gitsync: push failed ({message})", file=sys.stderr, flush=True)
