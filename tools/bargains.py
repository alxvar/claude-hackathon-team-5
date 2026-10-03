"""Bargain watcher: page Lucas when an ask on any venue is worth >= MIN_GAIN to us after the fee (Chief, Sat 11:10).

Every tick it reads every open venue's board (public, keyless) and, for each ask that sells cards for cash, our value of
those cards (GET /api/me/value, team key, cached CACHE_S): gain = our value - price - fee, the fee as the trader counts
it (agents/trader/loop.py): the venue's fee_bps / fee_per_card (the higher of current and pending), El Rastro's
ceil(5%) + 1 P per card. Epics and legendaries outside pages count too (RET-11 is worth 198 to us, RET-12 495). The
score a trade can add is capped at 50 [V, n=2], so the alert gives the gain and the capped gain, the cash it needs and
whether that keeps cash >= CASH_FLOOR. Once per offer, to ntfy `lucas`. It never buys and never writes to the game.

    source .env && python3 -u tools/bargains.py            # every tick (tools/daemons.sh start bargains)
    source .env && python3 tools/bargains.py --once --dry  # print what it would send
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
sys.path.insert(0, str(ROOT / "tools"))
from bazaar_sdk import Bazaar, BazaarError, _Http  # noqa: E402

URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
STATE = ROOT / "run" / "bargains_state.json"
HOUSE, HOUSE_FEE = "rastro", (500, 1)     # El Rastro: 5% + 1 P per card
MIN_GAIN = 20
SCORE_CAP = 50                            # per trade [V, n=2: LAV-05 and RET-01 closes, +50.0 each]
CACHE_S = 300                             # our value of a card, re-read this often (it moves with our holdings)
CASH_FLOOR = int(os.environ.get("CASH_FLOOR", 100))

try:
    from notify import notify as _notify
except Exception:  # noqa: BLE001
    _notify = None


def fee(price: int, cards: int, bps: int = HOUSE_FEE[0], per_card: int = HOUSE_FEE[1]) -> int:
    return math.ceil(int(price) * int(bps) / 10000) + int(per_card) * cards


def venue_fee(v: dict | None) -> tuple[int, int]:
    """(bps, per card): the higher of the current and the pending fee; El Rastro's when the venue is unknown."""
    if not v:
        return HOUSE_FEE
    p = v.get("pending_fee") or {}
    return (max(v.get("fee_bps") or 0, p.get("fee_bps") or 0), max(v.get("fee_per_card") or 0, p.get("fee_per_card") or 0))


class Api:
    """Public boards keyless, our value and offers with the team key; at most one team request a second."""

    def __init__(self, url: str, key: str):
        self.pub = _Http(url, {}, 15.0, False, 0)
        self.team = Bazaar(url, key, wait_on_tick=False, retries=0)
        self._last = 0.0

    def _team(self, fn, *a):
        wait = self._last + 1.0 - time.time()
        if wait > 0:
            time.sleep(wait)
        try:
            return fn(*a)
        finally:
            self._last = time.time()

    def clock(self):
        return self.pub._call("GET", "/api/clock")

    def venues(self):
        return self.pub._call("GET", "/api/venues")

    def board(self, venue):
        time.sleep(0.25)
        return self.pub._call("GET", f"/api/venues/{venue}/offers")

    def leaderboard(self):
        return self.pub._call("GET", "/api/leaderboard")

    def me(self):
        return self._team(self.team.me)

    def my_offers(self):
        return self._team(self.team.my_offers)

    def value(self, card):
        return self._team(self.team.value, card)


def load_state(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {"alerted": []}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    state["alerted"] = state.get("alerted", [])[-500:]
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state))
    tmp.replace(path)


class Watcher:
    def __init__(self, api, *, notifier=_notify, state_path: Path = STATE, cash_floor: int = CASH_FLOOR,
                 min_gain: float = MIN_GAIN, log=print, now=time.time):
        self.api, self.notifier, self.state_path = api, notifier, state_path
        self.cash_floor, self.min_gain, self.log, self.now = cash_floor, min_gain, log, now
        self.values: dict[str, tuple[float, float]] = {}
        self.state = load_state(state_path)

    def value(self, ref: str) -> float | None:
        hit = self.values.get(ref)
        if hit and self.now() - hit[1] < CACHE_S:
            return hit[0]
        try:
            v = float(self.api.value(ref)["your_value"])
        except (BazaarError, KeyError, TypeError, ValueError):
            return None
        self.values[ref] = (v, self.now())
        return v

    def scan(self, *, dry: bool = False) -> list[dict]:
        """One pass over every board: the bargains found (alerted unless dry or already alerted)."""
        me = self.api.me()
        mine = {o["id"] for o in self.api.my_offers().get("offers") or [] if o.get("maker") == me["id"]}
        venues = {v["venue"]: v for v in self.api.venues().get("venues") or [] if v.get("status") == "open"}
        venues.setdefault(HOUSE, None)
        teams = sorted(self.api.leaderboard().get("teams") or [], key=lambda t: -(t.get("score") or 0))
        top = {t["team"] for t in teams[:4]}
        found = []
        for vid, v in venues.items():
            try:
                offers = self.api.board(vid).get("offers") or []
            except BazaarError as e:
                self.log(f"bargains: board {vid} unavailable ({e.code})")
                continue
            for o in offers:
                give, want = o.get("give") or {}, o.get("want") or {}
                cards = [a for a in give.get("assets") or [] if isinstance(a, dict) and a.get("kind", "card") == "card"]
                if (o["id"] in mine or not cards or give.get("cash") or len(cards) != len(give.get("assets") or [])
                        or not want.get("cash") or want.get("assets") or want.get("types")
                        or o.get("to") not in (None, me["id"])):
                    continue                          # only cards for cash, takeable by us, not ours
                values = [self.value(a.get("ref")) for a in cards]
                if any(x is None for x in values):
                    continue
                price = int(want["cash"])
                f = fee(price, len(cards), *venue_fee(v)) if vid != HOUSE else fee(price, len(cards))
                value = sum(values)
                gain = value - price - f
                if gain < self.min_gain:
                    continue
                need = price + f
                b = {"offer": o["id"], "venue": vid, "venue_name": (v or {}).get("name", "El Rastro"),
                     "auto": ((v or {}).get("rules") or {}).get("mechanism") == "auto", "owner": (v or {}).get("owner"),
                     "refs": [a.get("ref") for a in cards], "rarity": [a.get("rarity") for a in cards], "price": price,
                     "fee": f, "value": round(value, 1), "gain": round(gain, 1), "score": round(min(gain, SCORE_CAP), 1),
                     "need": need, "cash": me.get("cash", 0), "to_us": o.get("to") == me["id"],
                     "fits": me.get("cash", 0) - need >= self.cash_floor, "top4_venue": (v or {}).get("owner") in top}
                found.append(b)
        found.sort(key=lambda b: -b["score"])
        for b in found:
            if dry or b["offer"] in self.state["alerted"]:
                continue
            self.alert(b)
            self.state["alerted"].append(b["offer"])
        if not dry:
            save_state(self.state_path, self.state)
        return found

    def alert(self, b: dict) -> None:
        refs = "+".join(b["refs"])
        title = f"BUY {refs} at {b['price']} P: +{b['score']:g} (worth {b['value']:g} to us)"
        how = (f"post a bid of {b['price']} P for {refs} on {b['venue_name']} ({b['venue']}, auto stall: the engine "
               f"crosses it)" if b["auto"] else f"accept offer {b['offer']} on {b['venue_name']} ({b['venue']})")
        lines = [f"{refs} ({', '.join(r or '?' for r in b['rarity'])}){' · addressed to us' if b['to_us'] else ''}",
                 f"Price {b['price']} + fee {b['fee']} = {b['need']} P. Our value {b['value']:g}: gain +{b['gain']:g}, "
                 f"score at most +{b['score']:g} (cap {SCORE_CAP}).",
                 f"Cash {b['cash']} → {b['cash'] - b['need']} after"
                 + (" (cash floor OK)" if b["fits"] else f": BELOW the cash floor {self.cash_floor}: needs a GUARDRAIL"),
                 f"To take it: {how}. No auto-buy: the Operator decides."]
        if b["top4_venue"]:
            lines.append(f"Venue owned by top-4 team {b['owner']}: the value created scores market points there.")
        body = "\n".join(lines)
        self.log(f"bargains: {title} | {body}")
        if self.notifier:
            self.notifier("lucas", title, body, priority=5 if b["score"] >= 40 else 4, tags=["moneybag", "eyes"])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry", action="store_true", help="print, send nothing, remember nothing")
    ap.add_argument("--min-gain", type=float, default=MIN_GAIN)
    args = ap.parse_args(argv)
    api = Api(URL, os.environ["BAZAAR_KEY"])
    w = Watcher(api, min_gain=args.min_gain)
    while True:
        try:
            c = api.clock()
            if c.get("paused") or c.get("doors") not in (None, "open"):
                if args.once:
                    return
                time.sleep(30)
                continue
            found = w.scan(dry=args.dry)
            print(f"{time.strftime('%H:%M:%S')} bargains: {len(found)} at >= {args.min_gain:g}"
                  + "".join(f" · {'+'.join(b['refs'])} {b['price']} (+{b['score']:g})" for b in found[:3]), flush=True)
            if args.once:
                return
            time.sleep(max(1.0, float(c.get("next_tick_in", 15))) + 1.0)
        except Exception as e:  # noqa: BLE001  a watcher keeps watching
            print(time.strftime("%H:%M:%S"), "bargains error:", repr(e)[:200], flush=True)
            if args.once:
                return
            time.sleep(15)


if __name__ == "__main__":
    main()
