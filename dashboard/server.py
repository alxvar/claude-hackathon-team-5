"""Read-only live dashboard for The Bazaar: every team's trades, offers and score, with insights.

    python dashboard/server.py              # then open http://127.0.0.1:8765
    python dashboard/server.py --port 9000  # another port
    python dashboard/server.py --no-key     # public data only (no score, assets or duels of ours)

It never writes to the game. Public routes (feed, leaderboard, El Rastro board, venues, catalog, schedule, levels,
dealers) are read without the team key; only `me` and `duels` use it. About 5-8 requests per tick, spaced 0.4 s
apart, so the team's 5 requests/s stay free for the live bots. The key comes from BAZAAR_KEY, the repo's .env or
~/bazaar_key.txt, stays in this process and is never printed; the page is served on 127.0.0.1 only. History is
cached in logs/dashboard/ (gitignored), so charts survive a restart.
"""
import argparse
import collections
import json
import math
import os
import statistics
import subprocess
import sys
import threading
import time
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bazaar-kit"))
from bazaar_sdk import Bazaar, BazaarError  # noqa: E402

HERE = Path(__file__).resolve().parent
CACHE = ROOT / "logs" / "dashboard"
TEAMS_MD = ROOT / "intel" / "teams.md"
URL = os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai")
GAP = 0.4          # seconds between two requests
EDGE = 3           # P of gain, after fees, that makes an offer an opportunity
RECENT = 30        # ticks that count as "recent" for momentum


def load_key():
    if os.environ.get("BAZAAR_KEY"):
        return os.environ["BAZAAR_KEY"].strip()
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("BAZAAR_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    f = Path.home() / "bazaar_key.txt"
    return f.read_text(encoding="utf-8").strip() if f.exists() else None


class Collector:
    """Polls the game once per tick and keeps everything it has seen, in memory and in logs/dashboard/."""

    def __init__(self, key):
        self.pub = Bazaar(URL, "", retries=2)
        self.pub._headers = {}  # public routes: don't spend the team's quota
        self.team = Bazaar(URL, key, retries=2, wait_on_tick=False) if key else None
        self.lock = threading.Lock()
        self.events = {}
        self.lb_hist = {}
        self.me_hist = []
        self.latest = {}
        self.errors = collections.deque(maxlen=15)
        self.requests = 0
        self.updated = None
        self.feed_gap = False
        self.teams_every = 0
        self.teams_push = False
        self.teams_last = 0.0
        CACHE.mkdir(parents=True, exist_ok=True)
        self._load()

    def _jsonl(self, name):
        p = CACHE / name
        if not p.exists():
            return []
        out = []
        for line in p.read_text(encoding="utf-8").splitlines():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        return out

    def _append(self, name, rows):
        if rows:
            with (CACHE / name).open("a", encoding="utf-8") as f:
                for r in rows:
                    f.write(json.dumps(r) + "\n")

    def _load(self):
        self.events = {e["id"]: e for e in self._jsonl("feed.jsonl")}
        self.lb_hist = {s["tick"]: s for s in self._jsonl("leaderboard.jsonl")}
        self.me_hist = self._jsonl("me.jsonl")

    def _get(self, name, fn):
        try:
            r = fn()
            self.requests += 1
            with self.lock:
                self.latest[name] = r
            return r
        except BazaarError as e:
            self.requests += 1
            self.errors.appendleft(f"{time.strftime('%H:%M:%S')} {name}: {e.code} {e.message[:120]}")
        except Exception as e:  # keep polling through anything
            self.errors.appendleft(f"{time.strftime('%H:%M:%S')} {name}: {e!r}"[:200])
        finally:
            time.sleep(GAP)
        return None

    def _ingest_feed(self, feed):
        evs = feed.get("events", [])
        with self.lock:
            known = max(self.events) if self.events else None
            fresh = [e for e in evs if e["id"] not in self.events]
            if known is not None and evs and min(e["id"] for e in evs) > known + 1:
                self.feed_gap = True  # we were away long enough to miss events
            for e in fresh:
                self.events[e["id"]] = e
        self._append("feed.jsonl", sorted(fresh, key=lambda e: e["id"]))

    def _ingest_lb(self, lb):
        tick = lb.get("snapshot_tick")
        if tick is None or tick in self.lb_hist:
            return
        snap = {"tick": tick, "t": lb.get("t"),
                "teams": {t["team"]: {"name": t.get("name"), "score": t.get("score"), "negotiating": t.get("negotiating"),
                                      "market": t.get("market"), "deals": t.get("deals")} for t in lb.get("teams", [])}}
        with self.lock:
            self.lb_hist[tick] = snap
        self._append("leaderboard.jsonl", [snap])

    def _ingest_me(self, me, tick):
        s = me.get("score") or {}
        row = {"tick": tick, "score": s.get("score"), "rank": s.get("rank"), "neg_points": s.get("neg_points"),
               "negotiating": s.get("negotiating"), "market": s.get("market"), "cash": me.get("cash"),
               "ladder_points": s.get("ladder_points"), "duel_points": s.get("duel_points")}
        with self.lock:
            if self.me_hist and self.me_hist[-1]["tick"] == tick:
                return
            self.me_hist.append(row)
        self._append("me.jsonl", [row])

    def write_teams(self):
        """Rewrite intel/teams.md and, with --push, commit and push that one file (retries on a busy git)."""
        try:
            text = Analysis(self).teams_md()
            TEAMS_MD.write_text(text, encoding="utf-8")
        except Exception as e:
            self.errors.appendleft(f"{time.strftime('%H:%M:%S')} teams.md: {e!r}"[:200])
            return
        if not self.teams_push:
            return
        git = ["git", "-C", str(ROOT)]
        rel = str(TEAMS_MD.relative_to(ROOT)).replace("\\", "/")
        for attempt in range(3):
            subprocess.run(git + ["add", "--", rel], capture_output=True)
            if subprocess.run(git + ["diff", "--cached", "--quiet", "--", rel]).returncode == 0:
                return
            c = subprocess.run(git + ["commit", "-q", "-m", f"intel: teams.md (Dani's dashboard, {time.strftime('%H:%M')})",
                                      "--", rel], capture_output=True, text=True)
            if c.returncode == 0:
                subprocess.run(git + ["pull", "--rebase", "--autostash", "-q", "origin", "main"], capture_output=True)
                p = subprocess.run(git + ["push", "-q", "origin", "HEAD:main"], capture_output=True, text=True)
                if p.returncode == 0:
                    return
                self.errors.appendleft(f"{time.strftime('%H:%M:%S')} teams.md push: {p.stderr.strip()[:150]}")
                return
            time.sleep(5)  # git busy (index.lock): try again
        self.errors.appendleft(f"{time.strftime('%H:%M:%S')} teams.md: git busy, will retry next round")

    def run(self):
        n = 0
        while True:
            clock = self._get("clock", self.pub.clock) or {}
            feed = self._get("feed", lambda: self.pub.feed(limit=500))
            if feed:
                self._ingest_feed(feed)
            lb_old = self.latest.get("leaderboard") or {}
            if n == 0 or clock.get("tick", 0) >= (lb_old.get("next_refresh_tick") or 0):
                lb = self._get("leaderboard", self.pub.leaderboard)
                if lb:
                    self._ingest_lb(lb)
            self._get("board", lambda: self.pub.board("rastro"))
            if self.team:
                me = self._get("me", self.team.me)
                if me:
                    self._ingest_me(me, clock.get("tick"))
                self._get("duels", self.team.duels)
                if n % 3 == 0:
                    self._get("duels_done", lambda: self.team.duels(done=True))
            if n % 10 == 0:
                for name, fn in (("catalog", self.pub.catalog), ("schedule", self.pub.schedule),
                                 ("levels", self.pub.levels), ("dealers", self.pub.dealers),
                                 ("venues", self.pub.venues)):
                    self._get(name, fn)
            self.updated = time.time()
            if self.teams_every and time.time() - self.teams_last >= self.teams_every and self.team:
                self.teams_last = time.time()
                self.write_teams()
            n += 1
            wait = float(clock.get("next_tick_in") or 30) + 1.0
            if clock.get("paused"):
                wait = 60
            time.sleep(min(65.0, max(5.0, wait)))


# ---------------------------------------------------------------------------------------------- analysis

def cash_of(side):
    return (side or {}).get("cash") or 0


def refs_of(side):
    """Card refs on one side of an offer: concrete assets, or wanted types ("card:LAV-09")."""
    side = side or {}
    out = [a.get("ref") for a in side.get("assets", []) if isinstance(a, dict) and a.get("kind", "card") == "card"]
    out += [t.split(":", 1)[1] for t in side.get("types", []) if isinstance(t, str) and t.startswith("card:")]
    return [r for r in out if r]


def set_of(ref):
    return ref.split("-")[0] if ref and "-" in ref else "?"


def median(xs):
    return statistics.median(xs) if xs else None


class Analysis:
    def __init__(self, c: Collector):
        with c.lock:
            self.events = sorted(c.events.values(), key=lambda e: e["id"])
            self.lb_hist = [c.lb_hist[k] for k in sorted(c.lb_hist)]
            self.me_hist = list(c.me_hist)
            L = dict(c.latest)
        self.c = c
        self.clock = L.get("clock") or {}
        self.lb = L.get("leaderboard") or {}
        self.board = (L.get("board") or {}).get("offers", [])
        self.me = L.get("me") or {}
        self.cat = L.get("catalog") or {}
        self.sched = L.get("schedule") or {}
        self.levels = (L.get("levels") or {}).get("levels", [])
        self.dealers = (L.get("dealers") or {}).get("personas", [])
        self.venues = (L.get("venues") or {}).get("venues", [])
        self.duels = (L.get("duels") or {}).get("duels", [])
        self.duels_done = (L.get("duels_done") or {}).get("duels", [])
        self.us = self.me.get("id") or "t05"
        self.names = {t["team"]: t.get("name", t["team"]) for t in self.lb.get("teams", [])}
        for d in self.dealers:
            self.names.setdefault(d["id"], d.get("name", d["id"]))
        self.aff = self.me.get("affinity") or {}
        rar = self.cat.get("rarities") or {}
        self.book = {k: v.get("book") for k, v in rar.items()}
        self.cards = {}
        for st in self.cat.get("sets", []):
            for cd in st.get("cards", []):
                if isinstance(cd, dict) and cd.get("id"):
                    self.cards[cd["id"]] = {"name": cd.get("name"), "rarity": cd.get("rarity"), "set": st.get("id")}
        self.marg = (self.cat.get("values") or {}).get("copy_marginals") or [1.0]
        self.held = collections.Counter(a.get("ref") for a in self.me.get("assets", []) if a.get("kind") == "card")
        self.held_value = collections.defaultdict(list)
        for a in self.me.get("assets", []):
            if a.get("kind") == "card" and a.get("your_value") is not None:
                self.held_value[a["ref"]].append(a["your_value"])
        rastro = next((v for v in self.venues if v.get("venue") == "rastro"), {})
        self.fee_bps = rastro.get("fee_bps", 500)
        self.fee_card = rastro.get("fee_per_card", 1)

    def name(self, tid):
        return self.names.get(tid, tid or "?")

    def rarity(self, ref):
        return (self.cards.get(ref) or {}).get("rarity")

    def fee(self, price, ncards=1):
        return math.ceil(price * self.fee_bps / 10000) + self.fee_card * ncards

    def value_more(self, ref):
        """Our private value of one more copy of `ref` (book × our affinity × copy marginal). An estimate."""
        r, s = self.rarity(ref), set_of(ref)
        if not r or s not in self.aff or not self.book.get(r):
            return None
        k = min(self.held.get(ref, 0), len(self.marg) - 1)
        return round(self.book[r] * self.aff[s] * self.marg[k], 1)

    def value_held(self, ref):
        v = self.held_value.get(ref)
        return min(v) if v else None

    # -------------------------------------------------------------------------------------- the pass over the feed
    def scan(self):
        self.maker = {}
        self.trades = []
        self.holder = {}
        self.threads = {}
        self.packs = collections.Counter()
        self.gifts = collections.Counter()
        self.listings = collections.Counter()
        self.bids = collections.defaultdict(collections.Counter)   # team -> set -> n bids posted
        self.asks = collections.defaultdict(collections.Counter)
        self.news = []
        self.duel_events = []
        for e in self.events:
            p, ty = e.get("payload") or {}, e.get("type", "")
            if ty == "offer.listed":
                o = p.get("offer") or {}
                who = e.get("actor") or o.get("maker")
                self.maker[o.get("id")] = who
                self.listings[who] += 1
                if cash_of(o.get("give")) and refs_of(o.get("want")):
                    for r in refs_of(o.get("want")):
                        self.bids[who][set_of(r)] += 1
                elif refs_of(o.get("give")) and cash_of(o.get("want")):
                    for r in refs_of(o.get("give")):
                        self.asks[who][set_of(r)] += 1
            elif ty == "settlement":
                items = [i for i in p.get("items", []) if i.get("kind") == "card" or i.get("ref")]
                kind = "dealer" if p.get("persona") else "team"
                self.trades.append({"tick": p.get("tick", e.get("tick")), "kind": kind, "dealer": p.get("persona"),
                                    "venue": p.get("venue"), "price": p.get("price") or 0, "fee": p.get("fee") or 0,
                                    "items": items, "parties": p.get("parties", [])})
                for i in items:
                    if i.get("id") is not None:
                        self.holder[i["id"]] = {"ref": i.get("ref"), "team": i.get("to"), "tick": p.get("tick"),
                                                "price": p.get("price"), "frm": i.get("frm")}
            elif ty == "thread.message" and p.get("kind") == "persona":
                th = self.threads.setdefault(p.get("thread"), {"team": p.get("team"), "dealer": p.get("with"),
                                                               "dealer_prices": [], "team_prices": [], "msgs": 0,
                                                               "side": None})
                th["msgs"] += 1
                o = p.get("offer") or {}
                if o:
                    mine = p.get("sender") == p.get("with")
                    gives, wants = cash_of(o.get("give")), cash_of(o.get("want"))
                    price = wants if mine and wants else gives if mine else gives if gives else wants
                    if mine:
                        th["side"] = "team buys" if wants else "team sells"
                    (th["dealer_prices"] if mine else th["team_prices"]).append(price)
            elif ty == "pack.opened":
                self.packs[p.get("team")] += 1
            elif ty == "gift.given":
                self.gifts[p.get("team")] += 1
            elif ty.startswith("duel"):
                self.duel_events.append(e)
            if ty.startswith(("level", "announcement", "schedule", "venue", "dealer")) or ty in ("set.released",):
                self.news.append({"tick": e.get("tick"), "type": ty, "text": json.dumps(p, ensure_ascii=False)[:220]})

    # -------------------------------------------------------------------------------------- per-team profiles
    def profiles(self):
        teams = sorted(self.lb.get("teams", []), key=lambda t: -(t.get("score") or 0))
        rank = {t["team"]: i + 1 for i, t in enumerate(teams)}
        hist = self.lb_hist
        then = None
        if hist:
            last = hist[-1]["tick"]
            older = [h for h in hist if h["tick"] <= last - RECENT]
            then = older[-1] if older else hist[0]
        our_rank = rank.get(self.us, 99)
        top_sets = {s for s, a in self.aff.items() if a >= 1.1}
        low_sets = {s for s, a in self.aff.items() if a < 1.0}
        out = []
        for t in teams:
            tid = t["team"]
            buys, sells, dbuys, dsells = (collections.Counter() for _ in range(4))
            team_trades = dealer_trades = 0
            volume = 0
            prices = []
            biggest = None
            for tr in self.trades:
                if tid not in tr["parties"]:
                    continue
                if tr["kind"] == "team":
                    team_trades += 1
                    volume += tr["price"]
                    prices.append(tr["price"])
                    if not biggest or tr["price"] > biggest["price"]:
                        biggest = tr
                else:
                    dealer_trades += 1
                for i in tr["items"]:
                    if i.get("kind", "card") != "card":
                        continue
                    s = i.get("set") or set_of(i.get("ref"))
                    if i.get("to") == tid:
                        (buys if tr["kind"] == "team" else dbuys)[s] += 1
                    elif i.get("frm") == tid:
                        (sells if tr["kind"] == "team" else dsells)[s] += 1
            interest = collections.Counter()
            for s, k in (buys + dbuys).items():
                interest[s] += 2 * k
            for s, k in self.bids[tid].items():
                interest[s] += k
            dumping = collections.Counter()
            for s, k in (sells + dsells).items():
                dumping[s] += 2 * k
            for s, k in self.asks[tid].items():
                dumping[s] += k
            net = {s: interest[s] - dumping[s] for s in set(interest) | set(dumping)}
            wants = [s for s, v in sorted(net.items(), key=lambda kv: -kv[1]) if v >= 2][:3]
            dumps = [s for s, v in sorted(net.items(), key=lambda kv: kv[1]) if v <= -2][:3]
            labels = []
            if wants:
                labels.append(f"Collects {'/'.join(wants)}")
            if team_trades >= 3:
                labels.append("Team trader")
            if dealer_trades >= 4 and dealer_trades >= 2 * team_trades:
                labels.append("Dealer grinder")
            if self.packs[tid] >= 3:
                labels.append("Pack opener")
            if self.listings[tid] >= 15:
                labels.append("Market maker")
            if team_trades + dealer_trades + self.listings[tid] < 3:
                labels.append("Quiet")
            relation = []
            if tid != self.us:
                comp = [s for s in wants if s in top_sets]
                buyer = [s for s in wants if s in low_sets]
                if comp:
                    relation.append(("rival", f"competes for {'/'.join(comp)}"))
                if buyer:
                    relation.append(("buyer", f"buys {'/'.join(buyer)} from us" +
                                     (" (below us: good)" if rank.get(tid, 0) > our_rank else " (above us)")))
                sup = [s for s in dumps if s in top_sets]
                if sup:
                    relation.append(("seller", f"sells {'/'.join(sup)}: source for us"))
            prev = (then or {}).get("teams", {}).get(tid, {}).get("score") if then else None
            out.append({
                "team": tid, "name": t.get("name"), "rank": rank[tid], "us": tid == self.us,
                "score": t.get("score"), "negotiating": t.get("negotiating"), "market": t.get("market"),
                "level": t.get("level"), "album": f"{t.get('album_filled')}/{t.get('album_slots')}",
                "pages": t.get("pages_complete"), "deals": t.get("deals"), "luck": t.get("luck"),
                "delta": round((t.get("score") or 0) - prev, 2) if prev is not None else None,
                "team_trades": team_trades, "dealer_trades": dealer_trades, "volume": volume,
                "avg_price": round(statistics.mean(prices), 1) if prices else None,
                "packs": self.packs[tid], "listings": self.listings[tid], "gifts": self.gifts[tid],
                "wants": wants, "dumps": dumps, "labels": labels, "relation": relation,
                "biggest": self.trade_text(biggest) if biggest else None,
            })
        self.rank = rank
        self.then = then
        return out

    def trade_text(self, tr):
        refs = ", ".join(i.get("ref", "?") for i in tr["items"]) or "cash"
        frm = tr["items"][0].get("frm") if tr["items"] else None
        to = tr["items"][0].get("to") if tr["items"] else None
        return f"{self.name(to)} bought {refs} from {self.name(frm)} for {tr['price']} P (tick {tr['tick']})"

    # -------------------------------------------------------------------------------------- the market
    def market(self):
        rows = []
        for o in self.board:
            if o.get("status") not in (None, "open"):
                continue
            team = self.maker.get(o.get("id"))
            give, want = o.get("give") or {}, o.get("want") or {}
            if cash_of(give) and refs_of(want):
                side, refs, price = "bid", refs_of(want), cash_of(give)
            elif refs_of(give) and cash_of(want):
                side, refs, price = "ask", refs_of(give), cash_of(want)
            else:
                side, refs, price = "swap", refs_of(give) + refs_of(want), cash_of(give) or cash_of(want)
            ref = refs[0] if refs else None
            row = {"id": o.get("id"), "team": team, "name": self.name(team) if team else "unknown",
                   "ours": team == self.us, "side": side, "ref": ref, "n": len(refs), "price": price,
                   "card": (self.cards.get(ref) or {}).get("name"), "rarity": self.rarity(ref), "set": set_of(ref),
                   "to": o.get("to"), "expires": o.get("expires_tick"), "created": o.get("created_tick"),
                   "value": None, "edge": None}
            if team != self.us and ref and len(refs) == 1:
                if side == "ask":
                    v = self.value_more(ref)
                    if v is not None:
                        row["value"], row["edge"] = v, round(v - price - self.fee(price), 1)
                elif side == "bid" and self.held.get(ref):
                    v = self.value_held(ref)
                    if v is not None:
                        row["value"], row["edge"] = v, round(price - v - self.fee(price), 1)
            rows.append(row)
        rows.sort(key=lambda r: (-(r["edge"] if r["edge"] is not None else -999), r["side"], r["ref"] or ""))
        return rows

    def prices(self):
        by_r = collections.defaultdict(list)
        by_rd = collections.defaultdict(list)
        last = {}
        for tr in self.trades:
            if len(tr["items"]) != 1:
                continue
            i = tr["items"][0]
            r = i.get("rarity") or self.rarity(i.get("ref"))
            (by_r if tr["kind"] == "team" else by_rd)[r].append(tr["price"])
            if tr["kind"] == "team":
                last[i.get("ref")] = tr["price"]
        order = ["common", "uncommon", "rare", "epic", "legendary"]
        rows = []
        for r in order:
            t, d = by_r.get(r, []), by_rd.get(r, [])
            if not t and not d:
                continue
            rows.append({"rarity": r, "book": self.book.get(r), "team_n": len(t), "team_median": median(t),
                         "team_min": min(t) if t else None, "team_max": max(t) if t else None,
                         "dealer_n": len(d), "dealer_median": median(d)})
        return rows, last

    def tape(self, n=40):
        out = []
        for tr in reversed(self.trades[-n:]):
            i = tr["items"][0] if tr["items"] else {}
            out.append({"tick": tr["tick"], "kind": tr["kind"], "venue": tr["venue"] or tr["dealer"],
                        "ref": ", ".join(x.get("ref", "?") for x in tr["items"]), "rarity": i.get("rarity"),
                        "buyer": self.name(i.get("to")), "seller": self.name(i.get("frm")), "price": tr["price"],
                        "ours": self.us in tr["parties"]})
        return out

    def holders(self):
        """Who holds the cards we want (from trades only: starting cards and pack pulls are invisible)."""
        wanted = {r for r in self.cards if set_of(r) in {s for s, a in self.aff.items() if a >= 1.1}}
        wanted |= {r for o in self.board if self.maker.get(o.get("id")) == self.us for r in refs_of(o.get("want"))}
        rows = collections.defaultdict(list)
        for aid, h in self.holder.items():
            if h["ref"] in wanted and h["team"] and h["team"] != self.us and h["team"].startswith("t"):
                rows[h["ref"]].append({"team": h["team"], "name": self.name(h["team"]), "tick": h["tick"],
                                       "price": h["price"], "from": self.name(h["frm"])})
        out = []
        for ref in sorted(rows, key=lambda r: -(self.value_more(r) or 0)):
            c = self.cards.get(ref) or {}
            out.append({"ref": ref, "card": c.get("name"), "rarity": c.get("rarity"), "value": self.value_more(ref),
                        "we_hold": self.held.get(ref, 0), "holders": rows[ref]})
        return out

    def abuela(self):
        per = collections.defaultdict(list)
        for th in self.threads.values():
            dp = th["dealer_prices"]
            if len(dp) < 1 or not dp[0]:
                continue
            first, lastp = dp[0], dp[-1]
            move = (first - lastp) / first if th["side"] == "team buys" else (lastp - first) / first
            per[(th["team"], th["dealer"])].append({"move": move, "msgs": th["msgs"], "side": th["side"]})
        rows = []
        for (tid, dealer), xs in per.items():
            rows.append({"team": tid, "name": self.name(tid), "dealer": dealer, "threads": len(xs),
                         "avg_move": round(100 * statistics.mean(x["move"] for x in xs), 1),
                         "best_move": round(100 * max(x["move"] for x in xs), 1),
                         "avg_msgs": round(statistics.mean(x["msgs"] for x in xs), 1), "us": tid == self.us})
        rows.sort(key=lambda r: -r["avg_move"])
        return rows

    def schedule(self):
        t_now, secs = self.clock.get("t_hours") or 0, self.clock.get("tick_seconds") or 60
        rows = []
        for e in (self.sched.get("upcoming") or [])[:10]:
            rows.append({"at": e.get("at_hours"), "eta_min": round((e.get("at_hours", 0) - t_now) * secs),
                         "action": e.get("action"), "note": e.get("note", ""),
                         "params": json.dumps(e.get("params") or {}, ensure_ascii=False)[:160]})
        return rows

    # -------------------------------------------------------------------------------------- insights
    def insights(self, prof, market):
        out = []

        def add(kind, text):
            out.append({"kind": kind, "text": text})

        byid = {p["team"]: p for p in prof}
        us = byid.get(self.us)
        if prof and us:
            lead = prof[0]
            if lead["team"] != self.us:
                add("info", f"We are #{us['rank']} with {us['score']:.1f}; {lead['name']} leads with {lead['score']:.1f} "
                            f"({lead['score'] - us['score']:+.1f}).")
            above = [p for p in prof if p["rank"] == us["rank"] - 1]
            if above:
                add("info", f"Next rung: {above[0]['name']} at {above[0]['score']:.1f} "
                            f"({above[0]['score'] - us['score']:.1f} above us).")
        movers = sorted([p for p in prof if p["delta"]], key=lambda p: -p["delta"])[:3]
        for p in movers:
            if p["delta"] >= 1:
                add("mover", f"{p['name']} {p['delta']:+.1f} in the last ~{RECENT} ticks"
                             + (f"; biggest team trade: {p['biggest']}" if p["biggest"] else "") + ".")
        sells = [r for r in market if r["side"] == "bid" and (r["edge"] or 0) >= EDGE]
        for r in sells[:5]:
            add("sell", f"SELL: {r['name']} bids {r['price']} P for {r['ref']} (offer #{r['id']}); "
                        f"our copy is worth {r['value']} → +{r['edge']} after the fee if we accept.")
        buys = [r for r in market if r["side"] == "ask" and (r["edge"] or 0) >= EDGE]
        for r in buys[:5]:
            add("buy", f"BUY: {r['name']} asks {r['price']} P for {r['ref']} (offer #{r['id']}); "
                       f"worth ~{r['value']} to us → +{r['edge']} after the fee.")
        ours = {r["ref"]: r for r in market if r["ours"] and r["side"] == "bid" and r["ref"]}
        rivals = collections.defaultdict(dict)
        for r in market:
            if r["side"] == "bid" and not r["ours"] and r["ref"] in ours:
                best = rivals[r["ref"]].get(r["name"])
                if not best or r["price"] > best["price"]:
                    rivals[r["ref"]][r["name"]] = r
        for ref, by in sorted(rivals.items(), key=lambda kv: -max(x["price"] for x in kv[1].values())):
            mine = ours[ref]
            xs = sorted(by.values(), key=lambda x: -x["price"])
            top = xs[0]
            who = ", ".join(f"{x['name']} {x['price']}" for x in xs)
            if top["price"] >= mine["price"]:
                add("rival", f"OUTBID on {ref}: {who} P vs our {mine['price']} (#{mine['id']}). Raise, or drop it.")
            else:
                add("rival", f"We lead on {ref} at {mine['price']} P (#{mine['id']}); also bidding: {who}.")
        rivals_by_set = collections.defaultdict(list)
        for p in prof:
            if p["us"]:
                continue
            for s in p["wants"]:
                if self.aff.get(s, 0) >= 1.1:
                    rivals_by_set[s].append(f"{p['name']} (#{p['rank']})")
        for s, who in rivals_by_set.items():
            add("rival", f"{len(who)} teams also collect {s} (worth {self.aff.get(s)}× to us): {', '.join(who)}. "
                         f"Expect competition for {s} cards; don't sell them {s}.")
        buyers = collections.defaultdict(list)
        for p in prof:
            for kind, text in p["relation"]:
                if kind == "buyer":
                    for s in p["wants"]:
                        if self.aff.get(s, 9) < 1.0:
                            buyers[s].append(f"{p['name']} (#{p['rank']})")
        for s, who in buyers.items():
            add("buyer", f"Who buys {s} (worth {self.aff.get(s)}× to us): {', '.join(who)}. Prefer teams below us.")
        ab = [r for r in self.abuela() if r["dealer"] == "abuela" and r["threads"] >= 2]
        if ab:
            best = ab[0]
            mine = next((r for r in ab if r["us"]), None)
            add("info", f"Best Abuela haggler: {best['name']}, {best['avg_move']}% off her first price on average"
                        + (f"; we get {mine['avg_move']}%." if mine else "."))
        if self.c.feed_gap:
            add("warn", "The feed had a gap (the dashboard was off for a while): counts before it are incomplete.")
        return out

    # -------------------------------------------------------------------------------------- why our score moved
    def our_trade_text(self, tr):
        i = tr["items"][0] if tr["items"] else {}
        refs = ", ".join(x.get("ref", "?") for x in tr["items"]) or "cash"
        if i.get("to") == self.us:
            return f"bought {refs} from {self.name(i.get('frm'))} for {tr['price']} P"
        return f"sold {refs} to {self.name(i.get('to'))} for {tr['price']} P"

    def story(self):
        """Per leaderboard interval: our score change = field drift (what idle teams did) + our own doing.

        The score is relative: teams that make no trade still move together when others gain. The median change
        of the teams that made no trade in the interval estimates that drift; the rest of our change is ours."""
        def neg_at(t):
            xs = [r for r in self.me_hist if r.get("tick") is not None and r["tick"] <= t and r.get("neg_points") is not None]
            return xs[-1]["neg_points"] if xs else None

        def rank_in(snap):
            order = sorted(snap["teams"], key=lambda k: -(snap["teams"][k].get("score") or 0))
            return order.index(self.us) + 1 if self.us in order else None

        out = []
        for a, b in zip(self.lb_hist, self.lb_hist[1:]):
            ta, tb = a["tick"], b["tick"]
            active, ours = set(), []
            for tr in self.trades:
                if ta < (tr["tick"] or 0) <= tb:
                    active.update(tr["parties"])
                    if self.us in tr["parties"]:
                        ours.append(tr)
            idle = [b["teams"][k]["score"] - a["teams"][k]["score"] for k in b["teams"]
                    if k in a["teams"] and k not in active and k != self.us
                    and b["teams"][k].get("score") is not None and a["teams"][k].get("score") is not None]
            usa, usb = a["teams"].get(self.us, {}).get("score"), b["teams"].get(self.us, {}).get("score")
            if usa is None or usb is None:
                continue
            drift = median(idle) if idle else 0.0
            delta = usb - usa
            na, nb = neg_at(ta), neg_at(tb)
            out.append({"from": ta, "to": tb, "score": usb, "rank": rank_in(b), "delta": round(delta, 2),
                        "drift": round(drift, 2), "ours": round(delta - drift, 2),
                        "neg_points": nb, "neg_delta": round(nb - na, 1) if na is not None and nb is not None else None,
                        "trades": [self.our_trade_text(t) for t in ours], "idle_teams": len(idle)})
        return out

    # -------------------------------------------------------------------------------------- intel/teams.md
    def team_prices(self, tid, market):
        """Median price per rarity a team traded at with other teams, plus its open bids."""
        by = collections.defaultdict(list)
        for tr in self.trades:
            if tr["kind"] == "team" and tid in tr["parties"] and len(tr["items"]) == 1:
                i = tr["items"][0]
                by[i.get("rarity") or self.rarity(i.get("ref"))].append(tr["price"])
        for r in market:
            if r["team"] == tid and r["side"] == "bid" and r["rarity"]:
                by[r["rarity"]].append(r["price"])
        return {k: median(v) for k, v in by.items() if v}

    def teams_md(self):
        """Rival profiles for the analysts (they read the first 6000 characters, so keep it tight)."""
        self.scan()
        prof = self.profiles()
        market = self.market()
        byid = {p["team"]: p for p in prof}
        us = byid.get(self.us, {})
        our_rank = us.get("rank", 99)
        first_tick = self.events[0].get("tick") if self.events else "?"
        ab = {r["team"]: r for r in self.abuela() if r["dealer"] == "abuela"}
        short = {"common": "c", "uncommon": "u", "rare": "r", "epic": "e", "legendary": "l"}
        L = [f"# Rival profiles (Dani's dashboard, auto {time.strftime('%a %H:%M')}, tick {self.clock.get('tick')})", "",
             f"_From the public feed since tick {first_tick}, the leaderboard and our /api/me. Inferred: starting cards "
             f"and pack pulls are invisible. Collects = sets it buys or bids for; dumps = sets it sells or asks for. "
             f"Prices = median of its team trades and open bids (c/u/r). Δ = score change over ~{RECENT} ticks._", "",
             "## Teams", ""]
        prices = {}
        for p in prof:
            tid = p["team"]
            tp = self.team_prices(tid, market)
            prices[tid] = tp
            if p["us"]:
                label = "US"
            elif p["rank"] <= 3:
                label = "leader (never feed)"
            elif p["wants"]:
                label = f"buyer for {'/'.join(p['wants'])}"
            elif p["dumps"]:
                label = f"seller of {'/'.join(p['dumps'])}"
            elif "Quiet" in p["labels"]:
                label = "inactive"
            else:
                label = "trader"
            bits = [f"#{p['rank']} {p['name']} {p['score']:.1f}"
                    + (f" (Δ {p['delta']:+.1f})" if p["delta"] is not None else ""), f"**{label}**"]
            if p["wants"]:
                bits.append("collects " + "/".join(p["wants"]))
            if p["dumps"]:
                bits.append("dumps " + "/".join(p["dumps"]))
            if tp:
                bits.append("prices " + " ".join(f"{short.get(k, k)} {v:g}" for k, v in sorted(tp.items(), key=lambda kv: list(short).index(kv[0]) if kv[0] in short else 9)))
            bits.append(f"{p['team_trades']} team / {p['dealer_trades']} dealer trades, {p['listings']} listings")
            if tid in ab:
                bits.append(f"Abuela −{ab[tid]['avg_move']:g}%")
            if p["biggest"] and p["biggest"].split(" bought ")[0] == p["name"]:
                bits.append("big: " + p["biggest"].split(" bought ", 1)[1])
            L.append("- " + " · ".join(bits))

        # who to sell what to: our cards, best counterparty below us
        copies = collections.defaultdict(list)
        for a in self.me.get("assets", []):
            if a.get("kind") == "card" and a.get("your_value") is not None:
                copies[a["ref"]].append(a["your_value"])
        all_med = collections.defaultdict(list)
        for tr in self.trades:
            if tr["kind"] == "team" and len(tr["items"]) == 1:
                all_med[tr["items"][0].get("rarity")].append(tr["price"])
        rows = []
        for ref, vals in copies.items():
            v = min(vals)
            rar, st = self.rarity(ref), set_of(ref)
            cands = []
            for p in prof:
                if p["us"] or p["rank"] <= 3:
                    continue
                bid = max((r["price"] for r in market if r["team"] == p["team"] and r["side"] == "bid" and r["ref"] == ref), default=None)
                if bid is None and st not in p["wants"]:
                    continue
                price = bid if bid is not None else (prices[p["team"]].get(rar) or median(all_med.get(rar, [])))
                if price is None:
                    continue
                gain = round(price - v - self.fee(price), 1)
                cands.append((p["rank"] > our_rank, bid is not None, gain, p, price))
            cands = [c for c in cands if c[2] >= EDGE]
            if not cands:
                continue
            cands.sort(key=lambda c: (c[0], c[1], c[2]), reverse=True)
            below, hasbid, gain, p, price = cands[0]
            also = ", ".join(f"{c[3]['name']} {c[4]:g}" for c in cands[1:4])
            rows.append((gain, f"| {ref} {rar[0] if rar else '?'} | {len(vals)} | {v:g} | {p['name']} (#{p['rank']}{'' if below else ', above us'}) "
                               f"| {price:g}{' bid' if hasbid else ' est.'} | {gain:+g} | {also or '—'} |"))
        rows.sort(key=lambda r: -r[0])
        L += ["", f"## Who to sell what to (us #{our_rank}; never the top 3)", "",
              "_Our copies (cheapest value), the best buyer, preferring teams BELOW us and an open bid over an estimate. "
              "Gain = price − our value − El Rastro fee (if we accept; 0 fee if they accept our ask)._", "",
              "| Card | Copies | Our value | Best buyer | Price | Gain | Also |", "|---|---|---|---|---|---|---|"]
        L += [r[1] for r in rows] or ["| — | | | no buyer above our value + 3 yet | | | |"]
        text = "\n".join(L) + "\n"
        if len(text) > 5900:  # the analysts read 6000 characters: drop the tail of the team list first
            head, rest = text.split("\n## Who to sell", 1)
            sell = "\n## Who to sell" + rest
            keep = 5900 - len(sell) - 40
            text = head[:keep].rsplit("\n", 1)[0] + "\n- … (more teams on the dashboard)\n" + sell
        return text

    def build(self):
        self.scan()
        prof = self.profiles()
        market = self.market()
        price_rows, last_price = self.prices()
        s = self.me.get("score") or {}
        us = next((p for p in prof if p["us"]), None)
        above = next((p for p in prof if us and p["rank"] == us["rank"] - 1), None)
        below = next((p for p in prof if us and p["rank"] == us["rank"] + 1), None)
        neighbours = [p["team"] for p in prof if us and abs(p["rank"] - us["rank"]) <= 2]
        return {
            "story": self.story(),
            "neighbours": neighbours,
            "above": {"name": above["name"], "score": above["score"], "rank": above["rank"]} if above else None,
            "below": {"name": below["name"], "score": below["score"], "rank": below["rank"]} if below else None,
            "lb_score": us["score"] if us else None, "lb_rank": us["rank"] if us else None,
            "now": time.strftime("%H:%M:%S"),
            "updated": datetime.fromtimestamp(self.c.updated).strftime("%H:%M:%S") if self.c.updated else None,
            "requests": self.c.requests, "errors": list(self.c.errors), "has_key": self.c.team is not None,
            "events_cached": len(self.events),
            "clock": {k: self.clock.get(k) for k in ("tick", "t_hours", "tick_seconds", "paused", "next_tick_in",
                                                     "closes", "opens", "limits")},
            "us": self.us,
            "me": {"cash": self.me.get("cash"), "level": self.me.get("level"), "collection_value": self.me.get("collection_value"),
                   "affinity": self.aff, "unlocked": self.me.get("unlocked"),
                   "album": f"{(self.me.get('album') or {}).get('filled')}/{(self.me.get('album') or {}).get('slots')}",
                   "score": {k: s.get(k) for k in ("score", "rank", "negotiating", "market", "neg_points", "ladder_points",
                                                   "duel_points", "bench_efficiency", "deals", "pages_complete", "luck")}},
            "me_hist": self.me_hist[-500:],
            "lb_hist": [{"tick": h["tick"], "scores": {k: v.get("score") for k, v in h["teams"].items()}}
                        for h in self.lb_hist],
            "names": self.names,
            "teams": prof,
            "insights": self.insights(prof, market),
            "market": market,
            "prices": price_rows,
            "tape": self.tape(),
            "holders": self.holders(),
            "abuela": self.abuela(),
            "schedule": self.schedule(),
            "levels": self.levels,
            "dealers": [{"id": d["id"], "name": d.get("name"), "status": d.get("status"), "level": d.get("level"),
                         "line": d.get("line") or d.get("teaser"), "open_to_us": d["id"] in (self.me.get("unlocked") or [])}
                        for d in self.dealers],
            "venues": [{k: v.get(k) for k in ("venue", "name", "owner_name", "status", "fee_bps", "trades", "volume",
                                              "traders")} for v in self.venues],
            "duels": self.duels, "duels_done": self.duels_done[-40:],
            "duel_events": [{"tick": e.get("tick"), "type": e.get("type"),
                             "text": json.dumps(e.get("payload"), ensure_ascii=False)[:200]} for e in self.duel_events[-30:]],
            "news": self.news[-20:][::-1],
        }


# ---------------------------------------------------------------------------------------------- web

class Handler(BaseHTTPRequestHandler):
    collector: Collector = None
    _cache = (0.0, b"")

    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._send(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
        if self.path.startswith("/api/data"):
            t, body = Handler._cache
            if time.time() - t > 3:
                try:
                    body = json.dumps(Analysis(self.collector).build(), default=str).encode()
                except Exception as e:  # show the error in the page instead of a blank screen
                    body = json.dumps({"fatal": repr(e)[:500]}).encode()
                Handler._cache = (time.time(), body)
            return self._send(200, body, "application/json")
        self._send(404, b"not found", "text/plain")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-key", action="store_true", help="public data only")
    ap.add_argument("--teams-every", type=int, default=600, help="seconds between intel/teams.md rewrites; 0 = off")
    ap.add_argument("--push", action="store_true", help="commit and push intel/teams.md after each rewrite")
    args = ap.parse_args()
    key = None if args.no_key else load_key()
    c = Collector(key)
    c.teams_every, c.teams_push = args.teams_every, args.push
    threading.Thread(target=c.run, daemon=True).start()
    Handler.collector = c
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Bazaar dashboard on http://127.0.0.1:{args.port}  (team key: {'yes' if key else 'no'}; read-only)", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
