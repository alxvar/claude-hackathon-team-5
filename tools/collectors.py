"""Who collects which set: the rule for every sale from our bots (Chief, Sat 11:50).

Value created is the buyer's value minus the seller's, at private values: a sale to a team that doesn't collect the
set scored -10.2 on our venue [V]. So a SELL may go only to a team that COLLECTS the card's set:
- `intel/teams.md` (Dani's dashboard) says "collects X/Y" for it, or
- the feed shows it bidding cash for a card of the set (at least half the card's book: Team 13's 2 P bids on RET
  commons are no sign) or asking a dealer to sell it one;
and never to a team that teams.md says "dumps" that set. Unknown → no.

    from collectors import Collectors
    ok, why = Collectors.load().allows("t07", "SAL")
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEAMS_MD, FEED = ROOT / "intel" / "teams.md", ROOT / "data" / "feed.jsonl"


def book_of(card: str) -> int:
    """Book price from the card number: every set numbers commons 01-05, uncommons 06-08, rares 09-10, the epic 11,
    the legendary 12 (catalog: CHA, SAL [V]; the other sets follow the same numbering [L])."""
    try:
        n = int(str(card).split("-")[1])
    except (IndexError, ValueError):
        return 10
    return 10 if n <= 5 else 25 if n <= 8 else 70 if n <= 10 else 180 if n == 11 else 450
_LINE = re.compile(r"^- #\d+ Team (\d+)\b(.*)$")


def set_of(card: str) -> str:
    return str(card).split("-")[0].upper()


def parse_teams_md(text: str) -> dict[str, dict[str, set]]:
    """{"t07": {"collects": {"LAV", "LAT"}, "dumps": {"MAL"}}} from the dashboard's team lines."""
    out: dict[str, dict[str, set]] = {}
    for line in text.splitlines():
        m = _LINE.match(line.strip())
        if not m:
            continue
        team = f"t{int(m.group(1)):02d}"
        prof = out.setdefault(team, {"collects": set(), "dumps": set()})
        for part in m.group(2).split("·"):
            part = part.strip().strip("*").strip()
            for key in ("collects", "dumps"):
                if part.startswith(key + " "):
                    prof[key] |= {s.strip().upper() for s in part[len(key) + 1:].split("/") if s.strip()}
    return out


def from_feed(events) -> dict[str, set]:
    """{team: sets it bid cash for (>= half book) or asked a dealer to sell} from feed events."""
    out: dict[str, set] = {}
    for e in events:
        p = e.get("payload") if isinstance(e.get("payload"), dict) else {}
        if e.get("type") == "offer.listed":
            o = p.get("offer") or {}
            team, give, want = o.get("maker") or e.get("actor"), o.get("give") or {}, o.get("want") or {}
            cards = [t[5:] for t in want.get("types") or [] if t.startswith("card:")] + list(want.get("cards") or [])
            if give.get("cash") and len(cards) == 1 and give["cash"] >= book_of(cards[0]) / 2:
                out.setdefault(team, set()).add(set_of(cards[0]))
        elif e.get("type") == "thread.opened" and p.get("kind") == "persona":
            card = ((p.get("topic") or {}).get("buy") or {}).get("card")
            if card:
                out.setdefault(p.get("team"), set()).add(set_of(card))
    return out


class Collectors:
    def __init__(self, teams: dict[str, dict[str, set]], feed: dict[str, set]):
        self.teams, self.feed = teams, feed

    @classmethod
    def load(cls, teams_md: Path = TEAMS_MD, feed: Path = FEED) -> "Collectors":
        try:
            teams = parse_teams_md(Path(teams_md).read_text())
        except OSError:
            teams = {}
        events = []
        try:
            with Path(feed).open() as f:
                for line in f:
                    try:
                        events.append(json.loads(line))
                    except ValueError:
                        continue
        except OSError:
            pass
        return cls(teams, from_feed(events))

    def allows(self, team: str | None, set_id: str) -> tuple[bool, str]:
        """(may we sell a card of `set_id` to `team`, why)."""
        if not team:
            return False, "no buyer named: a public ask can go to a team that doesn't collect the set"
        t = self.teams.get(team, {})
        if set_id in t.get("dumps", set()):
            return False, f"{team} dumps {set_id} (teams.md)"
        if set_id in t.get("collects", set()):
            return True, f"{team} collects {set_id} (teams.md)"
        if set_id in self.feed.get(team, set()):
            return True, f"{team} bid for or asked a dealer for {set_id} (feed)"
        return False, f"no sign that {team} collects {set_id}"


class CachedCollectors:
    """Collectors re-loaded at most every `every_s` seconds (teams.md is rewritten every 10 minutes)."""

    def __init__(self, every_s: float = 120.0, **paths):
        self.every_s, self.paths, self._c, self._at = every_s, paths, None, 0.0

    def get(self) -> Collectors:
        if self._c is None or time.time() - self._at > self.every_s:
            self._c, self._at = Collectors.load(**self.paths), time.time()
        return self._c
