"""Operator lock: exactly one Claude Code session operates the game at a time (plan §5; Friday two did at once).

run/operator.lock holds {pid, session, started, heartbeat}. The pid is the Claude Code process that runs the
command (the nearest `claude` ancestor; the parent shell if there is none), so the lock lives as long as the
session, not as long as this script. A lock is stale, and anyone may take it, when that pid is dead or its
heartbeat is more than 10 minutes old: the holder runs `heartbeat` on every wake-up.

    python3 tools/operator_lock.py acquire operator    # exit 1 (and who holds it) if another session does
    python3 tools/operator_lock.py heartbeat           # exit 1 if we are not the holder
    python3 tools/operator_lock.py status
    python3 tools/operator_lock.py release
"""
import fcntl
import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "run" / "operator.lock"
STALE_AFTER = 600  # seconds without a heartbeat


def owner_pid():
    """The Claude Code session behind this command: the nearest ancestor named `claude`, else our parent."""
    pid = os.getppid()
    for _ in range(20):
        try:
            out = subprocess.run(["ps", "-o", "ppid=,comm=", "-p", str(pid)], capture_output=True, text=True).stdout
            ppid, comm = out.strip().split(None, 1)
        except ValueError:
            break
        if os.path.basename(comm).lower() == "claude":
            return pid
        if int(ppid) <= 1:
            break
        pid = int(ppid)
    return os.getppid()


def alive(pid):
    try:
        os.kill(int(pid), 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except (TypeError, ValueError):
        return False
    return True


def read():
    try:
        return json.loads(LOCK.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def live(lock, now=None):
    """The holder is alive and has beaten within STALE_AFTER."""
    now = time.time() if now is None else now
    return bool(lock) and alive(lock.get("pid")) and now - lock.get("heartbeat", 0) <= STALE_AFTER


def _write(lock):
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    tmp = LOCK.with_suffix(".tmp")
    tmp.write_text(json.dumps(lock))
    os.replace(tmp, LOCK)


def _guard():
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    g = open(LOCK.with_suffix(".guard"), "w")
    fcntl.flock(g, fcntl.LOCK_EX)
    return g


def acquire(session_name, pid=None):
    """(ok, message). Refuses while another live session holds the lock; the same pid may re-acquire."""
    pid = pid or owner_pid()
    with _guard():
        cur = read()
        if live(cur) and cur.get("pid") != pid:
            return False, f"held by {describe(cur)}"
        now = time.time()
        _write({"pid": pid, "session": session_name, "started": now, "heartbeat": now,
                "started_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))})
        taken = f" (took over the stale lock of {describe(cur)})" if cur and cur.get("pid") != pid else ""
        return True, f"acquired by {session_name} (pid {pid}){taken}"


def heartbeat(pid=None):
    pid = pid or owner_pid()
    with _guard():
        cur = read()
        if not cur or cur.get("pid") != pid:
            return False, f"not the holder (lock: {describe(cur)})"
        cur["heartbeat"] = time.time()
        _write(cur)
        return True, f"heartbeat for {cur['session']} (pid {pid})"


def release(pid=None, force=False):
    pid = pid or owner_pid()
    with _guard():
        cur = read()
        if not cur:
            return True, "no lock"
        if cur.get("pid") != pid and live(cur) and not force:
            return False, f"not the holder (lock: {describe(cur)}); --force to remove it anyway"
        LOCK.unlink(missing_ok=True)
        return True, f"released {describe(cur)}"


def describe(lock):
    if not lock:
        return "none"
    age = time.time() - lock.get("heartbeat", 0)
    state = "LIVE" if live(lock) else ("STALE (pid dead)" if not alive(lock.get("pid")) else "STALE (no heartbeat)")
    return (f"{lock.get('session')} pid {lock.get('pid')} since {lock.get('started_at', '?')}, "
            f"last heartbeat {int(age)} s ago, {state}")


def main(argv):
    if not argv or argv[0] not in ("status", "acquire", "heartbeat", "release"):
        print(__doc__)
        return 2
    cmd = argv[0]
    if cmd == "status":
        print(describe(read()))
        return 0
    if cmd == "acquire":
        if len(argv) < 2:
            print("usage: operator_lock.py acquire <session name>")
            return 2
        ok, msg = acquire(argv[1])
    elif cmd == "heartbeat":
        ok, msg = heartbeat()
    else:
        ok, msg = release(force="--force" in argv)
    print(("OK: " if ok else "REFUSED: ") + msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
