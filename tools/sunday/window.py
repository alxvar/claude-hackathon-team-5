"""Duel windows (contra-ops #2, directive 07:05, Chief 07:15). Deterministic, keyless reads, no Claude prompt needed.

Every 60 s (15 s near a stop) it reads the keyless /api/clock and /api/schedule and recomputes each wave's time:
- Duels III: at D−5 min (game time: the clock's t_hours against the schedule's at_hours) it runs
  `tools/daemons.sh stop $WINDOW_STOP` (default "swaps opps recorder": directive 07:25, the trader keeps running) and
  checks with pgrep that none is left. During the wave it stops them again if anything brings them back. On
  `duels.finished` for "Duels III" (data/feed.jsonl, the collector's), or at D+65 min at the latest, it restarts only
  what it stopped, from run/floors.env, 15 s apart, in this order: trader (only if run/trader_ok exists, as t0.sh),
  opps (OPPS_BUILD=RET), swaps, recorder. No floors.env, no trader/opps restart: a bare start falls back to
  CASH_FLOOR=100.
- Final duels: the same stop at F−5 min; no restart after it. The sessions come from /api/schedule (`duels` actions;
  "Duels III" and "Final duels" are the seed), so a renamed or extra wave is handled in time order.
Safe to re-run: one instance (run/window.lock), and every step done is kept in run/window_state.json, so a second run
never repeats a restart. Started after a wave began: it stops at once; after it finished: it does nothing for it.

    tools/sunday/window.sh                 # the Operator arms it at 08:45 (logs/window.log)
    tools/sunday/window.sh --dry --once    # one look with the live clock and schedule; runs nothing
    tools/sunday/window.sh --status        # the state file and the next action
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
STATE, LOCK = ROOT / "run" / "window_state.json", ROOT / "run" / "window.lock"
FEED, FLOORS, TRADER_OK = ROOT / "data" / "feed.jsonl", ROOT / "run" / "floors.env", ROOT / "run" / "trader_ok"
DAEMONS = ROOT / "tools" / "daemons.sh"
PROCS = {"trader": "agents/trader/loop.py", "opps": "tools/opportunities.py", "swaps": "agents/trader/swaps.py",
         "recorder": "broker.record_bench"}            # daemons.sh name → what pgrep looks for; also the restart order
STOP = tuple((os.environ.get("WINDOW_STOP") or "swaps opps recorder").split())   # directive 07:25: not the trader
SEED = ("Duels III", "Final duels")   # the schedule's names; any other upcoming duel session joins in time order
LEAD_MIN, FALLBACK_MIN, EVERY_S, NEAR_S, GAP_S = 5, 65, 60, 15, 15


def log(msg: str) -> None:
    print(time.strftime("%H:%M:%S"), "window:", msg, flush=True)


def team_key() -> str | None:
    """BAZAAR_KEY from the environment, else from the repo's .env (window.sh is started without it). Never logged."""
    if os.environ.get("BAZAAR_KEY"):
        return os.environ["BAZAAR_KEY"]
    try:
        m = re.search(r"""^\s*(?:export\s+)?BAZAAR_KEY\s*=\s*["']?([^"'\s#]+)""", (ROOT / ".env").read_text(), re.M)
    except OSError:
        return None
    return m.group(1) if m else None


def get(path: str) -> dict | None:
    """GET with the team key first (Chief 11:45: the keyless 60/s per address is shared with every team on the venue
    Wi-Fi; two keyed reads a minute are nothing on our 5/s), then keyless. A missed read is the next look's."""
    key = team_key()
    for headers in ([{"X-Team-Key": key}] if key else []) + [{}]:
        try:
            req = urllib.request.Request(URL.rstrip("/") + path, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            log(f"GET {path} {'(team key)' if headers else '(keyless)'} failed: {type(e).__name__} "
                f"{getattr(e, 'code', '')}".rstrip())
    return None


def waves(state: dict, schedule: dict | None) -> list[tuple[str, bool]]:
    """[(session name, restart the bots after it)] in time order: SEED plus every upcoming `duels` action in
    /api/schedule (kept in run/window_state.json, so a wave that already fired stays). Never a restart after a Final."""
    names = state.setdefault("_waves", list(SEED))
    ups = sorted(((float(e["at_hours"]), (e.get("params") or {}).get("name")) for e in (schedule or {}).get("upcoming")
                  or [] if e.get("action") == "duels" and (e.get("params") or {}).get("name")))
    for _, n in ups:
        if n not in names:
            finals = [i for i, x in enumerate(names) if "final" in x.lower()]
            names.insert(finals[0] if finals and "final" not in n.lower() else len(names), n)
    return [(n, "final" not in n.lower()) for n in names]


def duel_at(schedule: dict | None, name: str) -> float | None:
    """The upcoming `duels` action's at_hours for `name`; None once it fired (or no schedule)."""
    for e in (schedule or {}).get("upcoming") or []:
        if e.get("action") == "duels" and (e.get("params") or {}).get("name") == name:
            return float(e["at_hours"])
    return None


def feed_events(name: str, path: Path | None = None) -> dict:
    """{"scheduled": t or None, "finished": t or None} for the duel session `name` in the collector's feed."""
    out = {"scheduled": None, "finished": None}
    try:
        with open(path or FEED) as f:
            for line in f:
                if '"duels.' not in line or name not in line:
                    continue
                e = json.loads(line)
                if (e.get("payload") or {}).get("name") == name and e.get("type") in ("duels.scheduled",
                                                                                   "duels.finished"):
                    out[e["type"].split(".")[1]] = e.get("t")
    except (OSError, ValueError):
        pass
    return out


def floors(path: Path | None = None) -> dict | None:
    """{"TRADER_FLOOR": int, "OPPS_FLOOR": int} from run/floors.env; None when missing or incomplete."""
    try:
        kv = dict(re.findall(r"^\s*([A-Z_]+)\s*=\s*(\d+)\s*$", Path(path or FLOORS).read_text(), re.M))
    except OSError:
        return None
    if not {"TRADER_FLOOR", "OPPS_FLOOR"} <= set(kv):
        return None
    return {k: int(v) for k, v in kv.items()}


class Ops:
    """The side effects, in one place (tests and --dry replace them)."""

    def __init__(self, dry: bool = False, sleep=time.sleep):
        self.dry, self.sleep, self.ran = dry, sleep, []

    def daemons(self, action: str, names, env: dict | None = None) -> None:
        cmd = ["bash", str(DAEMONS), action, *names]
        self.ran.append((action, tuple(names), dict(env or {})))
        if self.dry:
            log(f"DRY: {' '.join(f'{k}={v}' for k, v in (env or {}).items())} {' '.join(cmd[1:])}".strip())
            return
        r = subprocess.run(cmd, cwd=ROOT, env={**os.environ, **(env or {})}, capture_output=True, text=True,
                           timeout=120)
        for line in (r.stdout + r.stderr).strip().splitlines():
            log(f"  {line}")

    def left(self) -> list[str]:
        """Processes of the stopped bots still alive (pgrep)."""
        if self.dry:
            return []
        r = subprocess.run(["pgrep", "-fl", "|".join(PROCS[n] for n in STOP)], capture_output=True, text=True)
        return [x for x in r.stdout.strip().splitlines() if x]


def load_state(path: Path | None = None) -> dict:
    try:
        return json.loads(Path(path or STATE).read_text())
    except (OSError, ValueError):
        return {}


def save_state(state: dict, path: Path | None = None) -> None:
    path = Path(path or STATE)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1) + "\n")
    tmp.replace(path)


def stop(ops: Ops, why: str) -> None:
    log(f"STOP {' '.join(STOP)}: {why}")
    ops.daemons("stop", STOP)
    left = ops.left()
    log("pgrep: none left" if not left else f"pgrep: STILL RUNNING {left}: stop them by hand")


def restart(ops: Ops, why: str) -> str:
    """Only what STOP stopped, GAP_S apart, in PROCS order: trader (if run/trader_ok), opps (RET), swaps, recorder;
    the trader's and opps' floors from run/floors.env."""
    names = [n for n in PROCS if n in STOP]
    fl = floors() if {"trader", "opps"} & set(names) else {}
    if fl is None:
        log(f"NOT restarting ({why}): run/floors.env missing or without TRADER_FLOOR/OPPS_FLOOR (a bare start "
            "would use CASH_FLOOR=100): restart by hand")
        return "no floors.env"
    log(f"RESTART {' '.join(names)} ({why})" + (f" from run/floors.env {fl}" if fl else ""))
    for i, n in enumerate(names):
        if i:
            ops.sleep(GAP_S)
        if n == "trader":
            if TRADER_OK.exists():
                ops.daemons("restart", ["trader"], {"CASH_FLOOR": str(fl["TRADER_FLOOR"])})
            else:
                log("trader HELD: run/trader_ok missing (the rival-venue skip not confirmed)")
        elif n == "opps":
            ops.daemons("start", ["opps"], {"OPPS_BUILD": "RET", "CASH_FLOOR": str(fl["OPPS_FLOOR"])})
        else:
            ops.daemons("start", [n])
    return "restarted"


def step(state: dict, clock: dict | None, schedule: dict | None, ops: Ops, feed=feed_events) -> float:
    """One look: act on the first wave not done. → seconds to the next look."""
    if not clock or schedule is None:
        return EVERY_S
    t = clock.get("t_hours")
    running = clock.get("doors") == "open" and not clock.get("paused")
    for name, after in waves(state, schedule):
        w = state.setdefault(name, {"at": None, "stopped_t": None, "done": None})
        if w["done"]:
            continue
        at = duel_at(schedule, name)
        if at is not None:
            w["at"] = at                                    # recomputed every look while it's upcoming
        if w["stopped_t"] is None:
            if at is None:                                  # not upcoming: already fired, or not scheduled yet
                fe = feed(name)
                if fe["finished"] is not None:
                    w["done"] = f"finished before window.sh saw it (t {fe['finished']}): nothing to do"
                    log(f"{name}: {w['done']}")
                    continue
                if fe["scheduled"] is None:
                    return EVERY_S                          # not in the schedule nor the feed: wait
                w["at"] = w["at"] or fe["scheduled"]
                why = f"{name} already under way (scheduled at t {fe['scheduled']})"
            elif running and isinstance(t, (int, float)) and t >= at - LEAD_MIN / 60:
                why = f"{name} at t {at:.3f}, now t {t:.3f} (D−{LEAD_MIN} min)"
            else:
                near = running and isinstance(t, (int, float)) and at - t <= (LEAD_MIN + 10) / 60
                return NEAR_S if near else EVERY_S
            stop(ops, why)
            w["stopped_t"] = t
            if not after:
                w["done"] = f"stopped for {name}; no restart after it"
            return NEAR_S
        # stopped, waiting for the wave to end (Duels III only)
        fe = feed(name)
        late = isinstance(t, (int, float)) and w["at"] is not None and t >= w["at"] + FALLBACK_MIN / 60
        if fe["finished"] is not None or late:
            why = (f"duels.finished {name} (t {fe['finished']})" if fe["finished"] is not None
                   else f"no duels.finished by D+{FALLBACK_MIN} min (t {t:.3f})")
            w["done"] = restart(ops, why)
            return EVERY_S
        if ops.left():                                      # something came back inside the wave
            stop(ops, f"inside {name}: a stopped bot is running again")
        return NEAR_S
    return EVERY_S


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], allow_abbrev=False)
    ap.add_argument("--dry", action="store_true", help="read the live clock and schedule, run nothing, write no state")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args(argv)
    if not STOP or set(STOP) - set(PROCS):
        log(f"WINDOW_STOP {' '.join(STOP)!r}: only {', '.join(PROCS)} (space-separated): not arming")
        return 2
    if args.status:
        print(json.dumps(load_state(), indent=1))
        sched = get("/api/schedule")
        for name, after in waves(load_state(), sched):
            print(name, "at_hours", duel_at(sched, name), "| restart after:", after, "| feed", feed_events(name))
        print("stops:", " ".join(STOP), "(WINDOW_STOP)")
        clock = get("/api/clock") or {}
        print("clock: t_hours", clock.get("t_hours"), "doors", clock.get("doors"), "paused", clock.get("paused"))
        return 0
    if not args.dry:                                         # a dry look writes nothing: no lock needed
        lock = open(LOCK, "a+")
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            lock.seek(0)
            log(f"already running (lock {LOCK}: {lock.read().strip() or '?'}): not starting a second one")
            return 1
        lock.seek(0)
        lock.truncate()
        lock.write(f"pid {os.getpid()} since {time.strftime('%H:%M:%S')}\n")
        lock.flush()
    ops = Ops(dry=args.dry)
    state = {} if args.dry else load_state()
    log(f"armed (pid {os.getpid()}{', DRY' if args.dry else ''}): state {json.dumps(state)}")
    while True:
        wait = step(state, get("/api/clock"), get("/api/schedule"), ops)
        if not args.dry:
            save_state(state)
        if args.once or all((state.get(n) or {}).get("done") for n, _ in waves(state, None)):
            log(f"{'one look done' if args.once else 'all waves done'}: {json.dumps(state)}")
            return 0
        time.sleep(wait)


if __name__ == "__main__":
    sys.exit(main())
