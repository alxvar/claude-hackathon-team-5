"""Radio Rastro watcher: every news item into intel/news.md; the ones that name something we trade, to Lucas's phone.

The organisers' news (GET /api/news, keyless: sources boletin, radio, tablon) mixes true items ("the market moves as
they say") with rumours. Every tick this reads it and, for each new item, oldest first:
- appends it to intel/news.md (time, tick, source, headline, body, and what it names);
- prints one `NEWS ...` line (the Builder session relays each to the Chief of staff);
- pages Lucas (ntfy `lucas`) only when it names a dealer, a card, a set, a price, a venue or a game event (names from
  the live catalog, venues and dealers; event words in Spanish and English). Noise ("Atleti win 2-1") stays in the file.
Read-only: it never writes to the game.

    python3 -u tools/news.py             # every tick (tools/daemons.sh start news)
    python3 tools/news.py --once --dry   # print, write nothing
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
sys.path.insert(0, str(ROOT / "tools"))
from bazaar_sdk import _Http  # noqa: E402

URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
OUT, STATE = ROOT / "intel" / "news.md", ROOT / "run" / "news_state.json"
HEADER = ("# Radio Rastro: the organisers' news\n\n_Every item from GET /api/news (sources: boletin, radio, tablon), "
          "oldest first, appended by `tools/news.py`. Some are true (\"the market moves as they say\"), some are "
          "rumours: verify before acting. **Names:** what the item mentions that we trade (dealer, card, set, price, "
          "venue, event); none = noise._\n\n")
DEALERS = {"abuela", "abuela carmen", "chato", "el chato", "pilar", "dona pilar"}
EVENTS = ("duel", "duelo", "duelos", "market test", "bench", "subasta", "auction", "nivel", "level", "sobre", "sobres",
          "pack", "packs", "regalo", "gift", "grant", "nueva serie", "new set", "fee", "comision", "tasa", "bono", "bond",
          "precio", "precios", "price", "prices", "agotado", "agotada", "sold out", "stock", "escasez", "shortage")
CARD = re.compile(r"\b[A-Z]{3}-\d{2}\b")
PRICE = re.compile(r"\b\d+(?:[.,]\d+)?\s*(?:P|primas?|pesetas?|€|euros?)\b|\bP\s*\d+\b", re.I)

try:
    from notify import notify as _notify
except Exception:  # noqa: BLE001
    _notify = None


def fold(s: str) -> str:
    """Lowercase, accents off: "Doña Pilar" and "dona pilar" match."""
    return "".join(c for c in unicodedata.normalize("NFKD", s or "") if not unicodedata.combining(c)).lower()


def names(text: str, sets: dict[str, str], venues: dict[str, str]) -> list[str]:
    """What an item names that we trade: ['dealer abuela', 'card SAL-09', 'set SAL', 'price', 'venue v07', 'event duel']."""
    f = fold(text)
    words = set(re.findall(r"[a-z0-9]+", f))
    out = [f"dealer {d}" for d in sorted(DEALERS) if (d in words if " " not in d else d in f)]
    out += [f"card {c}" for c in sorted(set(CARD.findall(text or "")))]
    out += [f"set {sid}" for sid, name in sorted(sets.items())
            if sid.lower() in words or (len(fold(name)) > 4 and fold(name) in f)]
    if PRICE.search(text or ""):
        out.append("price")
    out += [f"venue {vid}" for vid, name in sorted(venues.items())
            if (vid in words and vid != "rastro") or (name and len(fold(name)) > 4 and fold(name) in f)]
    if "el rastro" in f and "venue rastro" not in out:
        out.append("venue rastro")
    out += [f"event {e}" for e in EVENTS if (e in words if " " not in e else e in f)][:3]
    return out


class Watcher:
    def __init__(self, pub, *, out: Path = OUT, state: Path = STATE, notifier=_notify, log=print, dry=False):
        self.pub, self.out, self.state_path, self.notifier, self.log, self.dry = pub, out, state, notifier, log, dry
        try:
            self.state = json.loads(state.read_text())
        except (OSError, ValueError):
            self.state = {"seen": 0}
        self.sets: dict[str, str] = {}
        self.venues: dict[str, str] = {}
        self._names_at = 0.0

    def refresh_names(self) -> None:
        if time.time() - self._names_at < 600 and self.sets:
            return
        self._names_at = time.time()
        try:
            self.sets = {s["id"]: s.get("name", "") for s in self.pub._call("GET", "/api/catalog").get("sets", [])}
        except Exception as e:  # noqa: BLE001
            self.log(f"news: catalog unavailable ({e!r})")
        try:
            self.venues = {v["venue"]: v.get("name", "") for v in self.pub._call("GET", "/api/venues").get("venues", [])}
        except Exception as e:  # noqa: BLE001
            self.log(f"news: venues unavailable ({e!r})")

    def poll(self) -> list[dict]:
        """New items, oldest first: written, printed, and paged when they name something."""
        items = self.pub._call("GET", "/api/news").get("news") or []
        new = sorted((n for n in items if (n.get("id") or 0) > self.state["seen"]), key=lambda n: n["id"])
        if not new:
            return []
        self.refresh_names()
        for n in new:
            n["names"] = names(f"{n.get('headline', '')} {n.get('body', '')}", self.sets, self.venues)
            line = (f"- {time.strftime('%a %H:%M')} · tick {n.get('tick')} (hour {n.get('at_hours')}) · "
                    f"{n.get('source_name') or n.get('source')} · **{n.get('headline', '')}** · {n.get('body', '')}"
                    f" · Names: {', '.join(n['names']) or 'none'}\n")
            self.log(f"NEWS #{n['id']} [{n.get('source')}] {n.get('headline')} :: {n.get('body')} :: "
                     f"names: {', '.join(n['names']) or 'none'}")
            if self.dry:
                continue
            if not self.out.exists():
                self.out.parent.mkdir(parents=True, exist_ok=True)
                self.out.write_text(HEADER)
            with self.out.open("a") as f:
                f.write(line)
            # no push (Chief 17:40: Lucas gets CRITICAL only); the Builder relays NEWS lines to the Chief
            self.state["seen"] = max(self.state["seen"], n["id"])
        if not self.dry:
            self.state_path.parent.mkdir(parents=True, exist_ok=True)
            self.state_path.write_text(json.dumps(self.state))
        return new


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry", action="store_true", help="print, write and send nothing")
    args = ap.parse_args(argv)
    pub = _Http(URL, {}, 15.0, False, 0)
    w = Watcher(pub, dry=args.dry)
    while True:
        try:
            w.poll()
            c = pub._call("GET", "/api/clock")
            wait = 30.0 if c.get("paused") or c.get("doors") not in (None, "open") else float(c.get("next_tick_in", 10))
        except Exception as e:  # noqa: BLE001  a watcher keeps watching
            print(time.strftime("%H:%M:%S"), "news error:", repr(e)[:200], flush=True)
            wait = 15.0
        if args.once:
            return
        time.sleep(max(2.0, wait + 1.0))


if __name__ == "__main__":
    main()
