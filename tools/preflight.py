"""API preflight: is every key in .env working right now? (plan §5: the $1 cap stopped the analysts 21:59-22:16)

BAZAAR_KEY: GET /api/me. ANTHROPIC_API_KEY: a 1-token Haiku call (~$0.0001), which shows a spend cap as
"You have reached your specified API usage limits". BROKER_KEY, if set: GET /api/broker/book. Then the clock, our
cash and the daemons. Read-only (GET only, one game request per second); never prints a key. Exit 1 on any FAIL.

    python3 tools/preflight.py
"""
import json
import os
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
from bazaar_sdk import Bazaar, BazaarError, Broker  # noqa: E402

HAIKU = "claude-haiku-4-5-20251001"
KEYS = ("BAZAAR_KEY", "ANTHROPIC_API_KEY", "BROKER_KEY")


def load_env(path=ROOT / ".env"):
    """KEY=VALUE and `export KEY=VALUE` lines of .env; the process environment fills what .env lacks."""
    env = {}
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.removeprefix("export ").split("=", 1)
            try:
                env[k.strip()] = " ".join(shlex.split(v, comments=True))  # as the shell reads it: quotes, # comments
            except ValueError:  # unbalanced quote
                env[k.strip()] = v.strip()
    for k in (*KEYS, "BAZAAR_URL"):
        if not env.get(k) and os.environ.get(k):
            env[k] = os.environ[k]
    return env


def redact(text, env):
    for k in KEYS:
        if env.get(k):
            text = text.replace(env[k], f"<{k}>")
    return text


def check_anthropic(key, timeout=20):
    body = json.dumps({"model": HAIKU, "max_tokens": 1, "messages": [{"role": "user", "content": "ping"}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, method="POST", headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            out = json.loads(r.read())
        return True, f"{out.get('model', HAIKU)} answered ({out.get('usage', {}).get('output_tokens', '?')} token)"
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read()).get("error", {})
            return False, f"HTTP {e.code} {err.get('type', '')}: {err.get('message', '')}"
        except Exception:
            return False, f"HTTP {e.code} {e.reason}"
    except Exception as e:
        return False, f"network: {e!r}"


def main():
    env = load_env()
    url = env.get("BAZAAR_URL") or "https://bazaar.causaprima.ai"
    fails, lines = 0, []

    def report(name, ok, msg):
        nonlocal fails
        fails += not ok
        lines.append(f"{'OK  ' if ok else 'FAIL'}  {name}: {redact(msg, env)}")

    me = None
    if env.get("BAZAAR_KEY"):
        try:
            me = Bazaar(url, env["BAZAAR_KEY"], retries=1).me()
            report("BAZAAR_KEY", True, f"GET /api/me as {me.get('id')} ({me.get('name', '')})")
        except BazaarError as e:
            report("BAZAAR_KEY", False, f"GET /api/me: {e.code} {e.message[:200]}")
    else:
        report("BAZAAR_KEY", False, "missing from .env")

    if env.get("ANTHROPIC_API_KEY"):
        report("ANTHROPIC_API_KEY", *check_anthropic(env["ANTHROPIC_API_KEY"]))
    else:
        report("ANTHROPIC_API_KEY", False, "missing from .env")

    if env.get("BROKER_KEY"):  # optional: only once we run a venue
        time.sleep(1)
        try:
            book = Broker(url, env["BROKER_KEY"], retries=1).book()
            report("BROKER_KEY", True, f"GET /api/broker/book: {len(book.get('offers', []))} offers")
        except BazaarError as e:
            report("BROKER_KEY", False, f"GET /api/broker/book: {e.code} {e.message[:200]}")

    time.sleep(1)
    try:
        with urllib.request.urlopen(url.rstrip("/") + "/api/clock", timeout=15) as r:  # public: no key spent
            c = json.loads(r.read())
        lines.append(f"clock: tick {c.get('tick')} · {c.get('tick_seconds')} s/tick · paused {c.get('paused')} · "
                     f"doors {c.get('doors')} · round {c.get('round')} ({c.get('round_name')}) · "
                     f"closes {c.get('closes')} · next opens {c.get('next_opens')}")
    except Exception as e:
        report("clock", False, f"GET /api/clock: {e!r}")
    if me:
        s = me.get("score") or {}
        lines.append(f"us: cash {me.get('cash')} P · level {me.get('level')} · score {s.get('score')} · "
                     f"rank {s.get('rank')}")

    d = subprocess.run(["bash", str(ROOT / "tools" / "daemons.sh"), "status"], capture_output=True, text=True)
    lines.append("daemons:\n" + "\n".join("  " + x for x in (d.stdout + d.stderr).strip().splitlines()))
    print(redact("\n".join(lines), env))
    print(f"preflight: {'FAIL (' + str(fails) + ')' if fails else 'all OK'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
