"""Bargain watcher: page Lucas when an ask on any venue is worth >= MIN_GAIN to us after the fee (Chief, Sat 11:10).

Every tick it reads every open venue's board (public, keyless) and, for each ask that sells cards for cash, our value of
those cards (GET /api/me/value, team key, cached CACHE_S): gain = our value - price - fee, the fee as the trader counts
it (agents/trader/loop.py): the venue's fee_bps / fee_per_card (the higher of current and pending), El Rastro's
ceil(5%) + 1 P per card. Epics and legendaries outside pages count too (RET-11 is worth 198 to us, RET-12 495). The
score a trade can add is capped at 50 [V, n=2], so the alert gives the gain and the capped gain, the cash it needs and
whether that keeps cash >= CASH_FLOOR. Once per offer, to ntfy `lucas`. It never buys and never writes to the game.

Underpriced asks (Chief, Sat 18:10): every scan (every 2 min) ranks every ask we may take (any venue but ours and
rival-owned ones: buying there credits a rival's market; asks addressed to us included) by gain = our value - price -
taker fee, writes intel/underpriced.md, and sends Dani an ACT (tools/alerts.py) when gain >= ACT_GAIN, the cost leaves
cash >= ACT_RESERVE and the seller is no rival; it closes DONE (we hold the card) or VOID once the ask leaves its board.

Arbitrage (Chief, Sat 15:50): an ask for card X at P1 on one venue below a LIVE bid for X at P2 on another. Each leg
scores at our value V of one more copy, capped at 50 per trade: buy = min(V - P1 - f1, 50), sell = min(P2 - V - f2,
50); flagged when their sum >= ARB_MIN (without the cap it is P2 - P1 - fees; review 16:15). Never a card that would
close our page (its V carries the bonus). Both legs follow tools/policy.py, failing closed (their gains unknown): no
top-5 team or rival (Team 13, 17) as seller or bidder, and a page card (01-10) only to a team >= 6 below us. The best ask per bid, an
unknown seller skipped, never our own venue (RULES: no trades on it). No speculative inventory: only while the bid is
live; the alert gives the loss if leg 2 fails. Once per (ask, bid): an `ARB ...` line in logs/bargains.log,
intel/arbitrage.md, and notify("operator") (stderr unless NTFY_OPERATOR is set). The Operator executes both legs.

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
FEED, ARB_OUT = ROOT / "data" / "feed.jsonl", ROOT / "intel" / "arbitrage.md"
ARB_MIN = 5                               # min net spread
UNDERPRICED, ACT_GAIN, ACT_RESERVE = ROOT / "intel" / "underpriced.md", 15, 100
SCAN_EVERY_S = 120                        # a full sweep of the boards every 2 min (Chief 18:10: be gentle)
import policy  # noqa: E402  tools/policy.py: rivals, page-closer gap 6
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


def wanted_card(want: dict) -> str | None:
    """The one card type a bid wants, or None."""
    cards = list(want.get("cards") or []) + [t[5:] for t in want.get("types") or [] if str(t).startswith("card:")]
    cards += [a.get("ref") for a in want.get("assets") or [] if isinstance(a, dict)]
    return cards[0] if len(cards) == 1 else None


def feed_view(path: Path = FEED) -> tuple[dict, dict]:
    """({offer id: maker}, {(team, card): asset ids}) from the collector's feed (holdings are a lower bound)."""
    makers, held = {}, {}
    try:
        lines = path.read_text().splitlines()
    except OSError:
        return makers, held
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        p = e.get("payload") if isinstance(e.get("payload"), dict) else {}
        if e.get("type") == "offer.listed":
            o = p.get("offer") or {}
            makers[o.get("id")] = o.get("maker") or e.get("actor")
            for a in (o.get("give") or {}).get("assets") or []:
                if isinstance(a, dict) and a.get("ref"):
                    held.setdefault((makers[o.get("id")], a["ref"]), set()).add(a.get("id"))
        elif e.get("type") == "settlement":
            for i in p.get("items") or []:
                if i.get("kind") == "card":
                    held.setdefault((i.get("to"), i.get("ref")), set()).add(i.get("id"))
                    held.get((i.get("frm"), i.get("ref")), set()).discard(i.get("id"))
    return makers, held


def page_card(card: str) -> bool:
    try:
        return 1 <= int(card.split("-")[1]) <= 10
    except (IndexError, ValueError):
        return False


def arbitrage(asks: dict, bids: dict, *, makers: dict, held: dict, teams: list, me: str, value=None,
              closes_ours=lambda card, v: False) -> list[dict]:
    """The best ask per live bid for the same card on another venue, scored per leg at our value V (capped at
    SCORE_CAP each), best first. asks/bids: {card: [{offer, venue, price, fee}]} (fee: what we pay taking that leg).
    `value(card)` -> V or None (no V: the uncapped spread)."""
    out = []
    for card, bl in bids.items():
        for b in bl:
            bidder = makers.get(b["offer"])          # their gain unknown: the policy skips the top 5 and rivals
            if not bidder or bidder == me or not policy.check(bidder, teams=teams, page_closer=page_card(card))[0]:
                continue                              # feeding rule failing closed: holdings are a lower bound
            best = None
            for a in asks.get(card, []):
                seller = makers.get(a["offer"])
                if a["venue"] == b["venue"] or not seller or seller == bidder or seller == me \
                        or not policy.check(seller, teams=teams)[0]:
                    continue
                net = b["price"] - a["price"] - a["fee"] - b["fee"]
                if net >= ARB_MIN and (best is None or net > best["net"]):
                    best = {"card": card, "ask": a, "bid": b, "seller": seller, "bidder": bidder, "net": net,
                            "need": a["price"] + a["fee"]}
            if best is None:
                continue
            v = value(card) if value else None
            if v is not None:
                if closes_ours(card, v):
                    continue                          # its bonus scores only once, and only if we keep it
                buy = min(v - best["ask"]["price"] - best["ask"]["fee"], SCORE_CAP)
                sell = min(best["bid"]["price"] - v - best["bid"]["fee"], SCORE_CAP)
                best.update(v=v, buy=round(buy, 1), sell=round(sell, 1), score=round(buy + sell, 1),
                            if_leg2_fails=round(buy, 1))
                if best["score"] < ARB_MIN:
                    continue
            out.append(best)
    out.sort(key=lambda x: -x.get("score", x["net"]))
    return out


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
        self.state.setdefault("arbs", [])
        self.feed_path, self.arb_out, self._feed, self._feed_at = FEED, ARB_OUT, ({}, {}), 0.0
        self.underpriced_path, self._clock = UNDERPRICED, {}

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
        venues = {v["venue"]: v for v in self.api.venues().get("venues") or []        # never our own venue (RULES)
                  if v.get("status") == "open" and v.get("owner") != me["id"]}
        venues.setdefault(HOUSE, None)
        teams = sorted(self.api.leaderboard().get("teams") or [], key=lambda t: -(t.get("score") or 0))
        top = {t["team"] for t in teams[:4]}
        riv = policy.rivals(teams, me["id"]) if teams else None
        found, rows, board_ids = [], [], set()
        asks, bids = {}, {}
        for vid, v in venues.items():
            try:
                offers = self.api.board(vid).get("offers") or []
            except BazaarError as e:
                self.log(f"bargains: board {vid} unavailable ({e.code})")
                continue
            for o in offers:
                board_ids.add(o["id"])
                give, want = o.get("give") or {}, o.get("want") or {}
                cards = [a for a in give.get("assets") or [] if isinstance(a, dict) and a.get("kind", "card") == "card"]
                bps, per = venue_fee(v) if vid != HOUSE else HOUSE_FEE
                if o["id"] not in mine and o.get("to") in (None, me["id"]):
                    if give.get("cash") and not give.get("assets") and wanted_card(want) and not want.get("cash"):
                        bids.setdefault(wanted_card(want), []).append(
                            {"offer": o["id"], "venue": vid, "price": int(give["cash"]),
                             "fee": fee(int(give["cash"]), 1, bps, per)})
                    elif len(cards) == 1 and len(give.get("assets") or []) == 1 and want.get("cash") \
                            and not give.get("cash") and not want.get("assets") and not want.get("types") \
                            and not want.get("cards"):
                        asks.setdefault(cards[0].get("ref"), []).append(
                            {"offer": o["id"], "venue": vid, "price": int(want["cash"]),
                             "fee": fee(int(want["cash"]), 1, bps, per)})
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
                if gain >= 0:                         # the underpriced report: every ask that would gain at all
                    rows.append({"offer": o["id"], "venue": vid, "owner": (v or {}).get("owner"),
                                 "refs": [a.get("ref") for a in cards], "price": price, "fee": f,
                                 "value": round(value, 1), "gain": round(gain, 1), "need": price + f,
                                 "to_us": o.get("to") == me["id"], "expires_tick": o.get("expires_tick")})
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
        counts: dict = {}
        for a in me.get("assets") or []:
            counts[a.get("ref")] = counts.get(a.get("ref"), 0) + 1
        if not dry:                                   # close the loop on our own ACTed offers (opps, swaps)
            try:
                import alerts
                alerts.sweep(open_offer_ids=mine, asset_ids={a["id"] for a in me.get("assets") or []}, counts=counts,
                             notifier=self.notifier, log=self.log)
                for a in alerts.open_acts("underpriced"):   # an underpriced ask gone from its board: DONE / VOID
                    if a["offer"] not in board_ids:
                        alerts.close(a["offer"], counts.get(a.get("want"), 0) > (a.get("want_n") or 0),
                                     notifier=self.notifier, log=self.log)
            except Exception as e:                    # noqa: BLE001  alerts never break the watcher
                self.log(f"bargains: alert sweep failed ({e!r})"[:200])
        try:
            self.underpriced(rows, me, riv, counts, dry=dry)
        except Exception as e:                        # noqa: BLE001  the report never breaks the watcher
            self.log(f"bargains: underpriced report failed ({e!r})"[:200])
        found.sort(key=lambda b: -b["score"])
        for b in found:
            if dry or b["offer"] in self.state["alerted"]:
                continue
            self.alert(b)
            self.state["alerted"].append(b["offer"])
        if bids and asks:
            try:
                if self.now() - self._feed_at > 60:
                    self._feed, self._feed_at = feed_view(self.feed_path), self.now()
                aff = me.get("affinity") or {}

                def closes_ours(card, v):           # V above book x m: it carries our page bonus
                    from collectors import book_of
                    return v > book_of(card) * aff.get(card.split("-")[0], 1.0) + 0.5
                for x in arbitrage(asks, bids, makers=self._feed[0], held=self._feed[1], teams=teams, me=me["id"],
                                   value=self.value, closes_ours=closes_ours):
                    key = f"{x['ask']['offer']}:{x['bid']['offer']}"
                    if dry:
                        self.log(f"ARB (dry) {x['card']}: {json.dumps(x)[:300]}")
                    elif key not in self.state["arbs"]:
                        self.alert_arb(x, venues, me)
                        self.state["arbs"].append(key)
                self.state["arbs"] = self.state["arbs"][-500:]
            except Exception as e:                    # noqa: BLE001  the bargain state is still saved
                self.log(f"bargains: arbitrage failed ({e!r})"[:300])
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
        # log only (Chief 17:40: Lucas gets CRITICAL only; the Operator reads logs/bargains.log)


    def underpriced(self, rows: list, me: dict, riv, counts: dict, *, dry: bool = False) -> list:
        """Rank every gainful ask (rival-owned venues out), write intel/underpriced.md, ACT the strong ones."""
        if riv is None:                               # no leaderboard: we can't tell rivals, so nothing goes out
            self.log("bargains: leaderboard unknown: no underpriced report")
            return []
        makers = self._feed[0] if self._feed[0] else feed_view(self.feed_path)[0]
        ok = sorted((r for r in rows if r["owner"] not in riv), key=lambda r: -r["gain"])
        cash = me.get("cash", 0)
        L = [f"# Underpriced asks ({time.strftime('%a %H:%M')})", "",
             f"_Every ask we may take (El Rastro, v15 and other venues not owned by a rival; addressed to us included), "
             f"gain = our value - price - taker fee. ACT to Dani at gain >= {ACT_GAIN}, cost <= cash - {ACT_RESERVE} "
             f"(cash {cash}), seller no rival. `tools/bargains.py`, every 2 min._", "",
             "| gain | card | price + fee | our value | venue | seller | offer | note |", "|---|---|---|---|---|---|---|---|"]
        for r in ok[:25]:
            seller = makers.get(r["offer"]) or "?"
            note = ("to us; " if r["to_us"] else "") + ("rival seller" if seller in riv else "")
            L.append(f"| +{r['gain']:g} | {'+'.join(r['refs'])} | {r['price']} + {r['fee']} | {r['value']:g} | "
                     f"{r['venue']} | {seller} | {r['offer']} | {note.strip('; ')} |")
        if not ok:
            L.append("| | none | | | | | | |")
        if not dry:
            self.underpriced_path.parent.mkdir(parents=True, exist_ok=True)
            self.underpriced_path.write_text("\n".join(L) + "\n")
            import alerts
            for r in ok:
                seller = makers.get(r["offer"])
                if r["gain"] < ACT_GAIN or r["need"] > cash - ACT_RESERVE or not seller or seller in riv \
                        or len(r["refs"]) != 1:
                    continue
                until = None
                if r.get("expires_tick") is not None and self._clock.get("tick") is not None:
                    until = alerts.until_ts(r["expires_tick"], self._clock["tick"], self._clock.get("tick_seconds"))
                ref = r["refs"][0]
                alerts.act(f"BUY {ref} at {r['price']} P on {r['venue']} (+{r['gain']:g})", r["offer"],
                           until or time.time() + 600,
                           f"Offer {r['offer']} on {r['venue']}: {ref} for {r['price']} P + fee {r['fee']}; worth "
                           f"{r['value']:g} to us. Operator: accept it.", source="underpriced", want=ref,
                           want_n=counts.get(ref, 0), notifier=self.notifier, log=self.log)
        return ok

    def alert_arb(self, x: dict, venues: dict, me: dict) -> None:
        a, b = x["ask"], x["bid"]
        def how(leg, side):
            auto = ((venues.get(leg["venue"]) or {}).get("rules") or {}).get("mechanism") == "auto"
            if auto:
                return (f"post {'a bid' if side == 'buy' else 'an ask'} at {leg['price']} P on {leg['venue']} (auto "
                        f"stall: the engine crosses it; one more tick, fee unverified)")
            return f"accept offer {leg['offer']} on {leg['venue']}"
        gain = x.get("score", x["net"])
        title = f"ARB {x['card']}: buy {a['price']} ({a['venue']}) → sell {b['price']} ({b['venue']}): +{gain:g}"
        body = (f"1) BUY: {how(a, 'buy')} (seller {x['seller'] or '?'}, fee {a['fee']}). "
                f"2) next tick, SELL: {how(b, 'sell')} (bidder {x['bidder']}, fee {b['fee']}). "
                f"Needs {x['need']} P now (cash {me.get('cash', 0)}, floor {self.cash_floor}). Spread "
                f"{b['price']} - {a['price']} - fees {a['fee'] + b['fee']} = +{x['net']}"
                + (f"; scored at our value {x['v']:g}: buy {x['buy']:+g}, sell {x['sell']:+g} (cap {SCORE_CAP} each); "
                   f"if leg 2 fails we keep the card at {x['if_leg2_fails']:+g}" if "v" in x else "")
                + ". Check the bid is still live before buying; no speculative inventory.")
        self.log(f"{title} | {body}")
        try:
            new = not self.arb_out.exists()
            with self.arb_out.open("a") as f:
                if new:
                    f.write("# Arbitrage: asks below live bids (tools/bargains.py)\n\n_Each line: buy leg, sell leg, net "
                            "after both fees. The Operator executes both legs (2 accepts, 2 ticks)._\n\n")
                f.write(f"- {time.strftime('%a %H:%M')} · {title} · {body}\n")
        except OSError:
            pass
        if self.notifier:
            self.notifier("operator", title, body, priority=4, tags=["arrows_counterclockwise"])


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
            w._clock = c
            found = w.scan(dry=args.dry)
            print(f"{time.strftime('%H:%M:%S')} bargains: {len(found)} at >= {args.min_gain:g}"
                  + "".join(f" · {'+'.join(b['refs'])} {b['price']} (+{b['score']:g})" for b in found[:3]), flush=True)
            if args.once:
                return
            time.sleep(SCAN_EVERY_S)                  # every 2 min (Chief 18:10)
        except Exception as e:  # noqa: BLE001  a watcher keeps watching
            print(time.strftime("%H:%M:%S"), "bargains error:", repr(e)[:200], flush=True)
            if args.once:
                return
            time.sleep(15)


if __name__ == "__main__":
    main()
