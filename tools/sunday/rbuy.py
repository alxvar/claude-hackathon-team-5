"""Reactor BUY (Chief 21:32): take ONE offer as taker if: team seller (feed's offer.listed), venue not rival-owned,
first copy for us (we hold none), gain = /api/me/value − price − fee ≥ 15, cash ≥ 350 after, cash-only want.
    python3 rbuy.py OFFER_ID [--dry]"""
import json, math, os, sys, time
ROOT = "/Users/lucaswiese/Documents/claude-hackathon-team-5"
sys.path.insert(0, ROOT + "/bazaar-kit"); sys.path.insert(0, ROOT + "/tools")
from bazaar_sdk import Bazaar  # noqa: E402
import policy  # noqa: E402

oid, dry = int(sys.argv[1]), "--dry" in sys.argv
b = Bazaar(os.environ["BAZAAR_URL"], os.environ["BAZAAR_KEY"], wait_on_tick=False, timeout=8.0)
listed = None
for line in open(ROOT + "/data/feed.jsonl"):
    if f'"id": {oid},' in line and "offer.listed" in line:
        listed = json.loads(line)["payload"]["offer"]
if not listed: sys.exit(f"offer {oid} not in the feed (collector lag?)")
_r = [a.get("ref","") for a in (listed.get("give") or {}).get("assets",[])] + [t.split(":",1)[1] for t in (listed.get("give") or {}).get("types",[]) if t.startswith("card:")]
if any(x.startswith(("CHA-","MAL-")) for x in _r): sys.exit("BUY refused: CHA/MAL go only through the books (directive 07:05)")
venues = {v["venue"]: v for v in b._call("GET", "/api/venues")["venues"]}
v = venues.get(listed["venue"]) or {}
lb = b._call("GET", "/api/leaderboard"); teams = lb.get("teams") if isinstance(lb, dict) else lb
bad = policy.rivals(teams) | policy.RIVALS
g, w = listed.get("give") or {}, listed.get("want") or {}
refs = [a.get("ref") for a in g.get("assets", [])] + [t.split(":", 1)[1] for t in g.get("types", []) if t.startswith("card:")]
price = int(w.get("cash") or 0)
fee = math.ceil((v.get("fee_bps") or 0) * price / 10000) + (v.get("fee_per_card") or 0) * len(refs)
me = b.me()
held = {a["ref"] for a in me["assets"]}
val = sum(float(b.value(r)["your_value"]) for r in refs) if refs else 0
gain = val - price - fee
checks = {"not CHA/MAL (books only)": not any(policy.book_only(r) for r in refs), "one card": len(refs) == 1, "first copy": bool(refs) and not any(r in held for r in refs),
          "cash only": not w.get("assets") and not w.get("types") and not g.get("cash"),
          "team seller": str(listed.get("maker", "")).startswith("t") and listed.get("maker") != "t05",
          "not rival venue": v.get("owner") not in bad, "gain >= 15": gain >= 15,
          "cash >= 350 after": me["cash"] - price - fee >= 350, "open or to us": listed.get("to") in (None, "t05")}
print(json.dumps({"offer": oid, "card": refs, "maker": listed.get("maker"), "venue": listed["venue"], "owner": v.get("owner"),
                  "price": price, "fee": fee, "value": val, "gain": round(gain, 1), "cash": me["cash"], "checks": checks}))
if not all(checks.values()): sys.exit("BUY refused: " + ", ".join(k for k, ok in checks.items() if not ok))
if dry: sys.exit("dry run: all checks pass")
r = b.accept(oid); print(time.strftime("%H:%M:%S"), "ACCEPTED", json.dumps(r)[:300])
