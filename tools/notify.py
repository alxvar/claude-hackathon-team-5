"""Push a phone notification through ntfy.sh. Standard library only; never raises.

    python3 tools/notify.py <channel> "<title>" "<message>" [--priority 1-5] [--tags a,b] [--click URL]

The topic comes from env NTFY_<CHANNEL> (NTFY_DANI, NTFY_LUCAS); if it is unset the message goes to stderr instead and
notify() returns False. The same (channel, title) is sent at most once per 10 minutes (state in
run/notify_state.json), so a looping caller can't spam a phone. Messages are published as JSON to the server root
(env NTFY_URL, default https://ntfy.sh), which keeps accents and emoji out of HTTP headers.
"""
import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "run" / "notify_state.json"
REPEAT_S = 600  # identical (channel, title) at most once per 10 minutes


def _load(path):
    try:
        state = json.loads(path.read_text())
        return state if isinstance(state, dict) else {}
    except Exception:
        return {}


def _save(path, state, now):
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        state = {k: v for k, v in state.items() if isinstance(v, (int, float)) and now - v < 86400}  # keep it small
        tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
        tmp.write_text(json.dumps(state, indent=0))
        os.replace(tmp, path)  # atomic: several processes (opportunities, duel_monitor) share this file
    except Exception as e:
        print(f"notify: could not save state ({e!r})", file=sys.stderr)


def _post(url, body, timeout=10):
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status


def notify(channel, title, message, priority=3, tags=None, click=None, *, state_path=None, now=None):
    """Send one notification. True if ntfy accepted it; False if the topic is unset, the same (channel, title) went out
    in the last 10 minutes, or the request failed. Never raises."""
    try:
        state_path = Path(state_path) if state_path else STATE
        now = time.time() if now is None else now
        topic = os.environ.get(f"NTFY_{channel.upper()}", "").strip()
        if not topic:
            print(f"notify[{channel}] (NTFY_{channel.upper()} unset) {title}\n{message}", file=sys.stderr)
            return False
        key = f"{channel.lower()}|{title}"
        state = _load(state_path)
        last = state.get(key)
        if isinstance(last, (int, float)) and now - last < REPEAT_S:
            print(f"notify[{channel}] suppressed (sent {int(now - last)} s ago): {title}", file=sys.stderr)
            return False
        body = {"topic": topic, "title": title, "message": message, "priority": int(max(1, min(5, priority)))}
        if tags:
            body["tags"] = list(tags) if not isinstance(tags, str) else [t for t in tags.split(",") if t]
        if click:
            body["click"] = click
        status = _post(os.environ.get("NTFY_URL", "https://ntfy.sh").rstrip("/") + "/", body)
        if not 200 <= status < 300:
            print(f"notify[{channel}] ntfy answered HTTP {status}: {title}", file=sys.stderr)
            return False
        state[key] = now
        _save(state_path, state, now)
        return True
    except Exception as e:  # a notification must never take its caller down
        print(f"notify[{channel}] failed ({e!r}): {title}", file=sys.stderr)
        return False


def main(argv=None):
    ap = argparse.ArgumentParser(description="Send a push notification via ntfy.sh")
    ap.add_argument("channel", help="dani, lucas, ... → env NTFY_<CHANNEL>")
    ap.add_argument("title")
    ap.add_argument("message")
    ap.add_argument("--priority", type=int, default=3)
    ap.add_argument("--tags", default=None, help="comma-separated ntfy tags")
    ap.add_argument("--click", default=None, help="URL opened when the notification is tapped")
    a = ap.parse_args(argv)
    ok = notify(a.channel, a.title, a.message, a.priority, a.tags, a.click)
    print("sent" if ok else "not sent")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
