"""DENY buy (Chief 19:05): take ONE card as taker on the Chief's "DENY <card> <offer id>" line only.
Cap 35 P fee included, cash floor 85 (this rule only), team seller only, never on a rival-owned venue.
    python3 deny.py SAL-06 15011 [--dry]"""
import json, math, os, sys, time, urllib.request
ROOT = "/Users/lucaswiese/Documents/claude-hackathon-team-5"
sys.path.insert(0, ROOT + "/bazaar-kit"); sys.path.insert(0, ROOT + "/tools")
from bazaar_sdk import Bazaar  # noqa: E402
import policy  # noqa: E402

card, oid, dry = sys.argv[1], int(sys.argv[2]), "--dry" in sys.argv
url, key = os.environ["BAZAAR_URL"], os.environ["BAZAAR_KEY"]
b = Bazaar(url, key, wait_on_tick=False, timeout=8.0)
listed = None
for line in open(ROOT + "/data/feed.jsonl"):
    if f'"id": {oid},' in line and "offer.listed" in line:
        listed = json.loads(line)["payload"]["offer"]
if not listed:
    for o in b.my_offers().get("offers", []):
        if o.get("id") == oid: listed = o
if not listed: sys.exit(f"offer {oid} not found in feed or my offers")
venues = {v["venue"]: v for v in b._call("GET", "/api/venues")["venues"]}
v = venues.get(listed["venue"]) or {}
lb = b._call("GET", "/api/leaderboard"); teams = lb.get("teams") if isinstance(lb, dict) else lb
bad = policy.rivals(teams) | policy.RIVALS
g, w = listed.get("give") or {}, listed.get("want") or {}
refs = [a.get("ref") for a in g.get("assets", [])] + [t.split(":", 1)[1] for t in g.get("types", []) if t.startswith("card:")]
price = int(w.get("cash") or 0)
fee = math.ceil((v.get("fee_bps") or 0) * price / 10000) + (v.get("fee_per_card") or 0) * len(refs)
me = b.me()
checks = {"card matches": refs == [card], "cash only": not w.get("assets") and not w.get("types") and not g.get("cash"),
          "team seller": str(listed.get("maker", "")).startswith("t") and listed.get("maker") != "t05",
          "not rival venue": v.get("owner") not in bad, "price+fee <= 35": price + fee <= 35,
          "cash >= 350 after": me["cash"] - price - fee >= 350, "addressed to us or open": listed.get("to") in (None, "t05")}
print(json.dumps({"offer": oid, "maker": listed.get("maker"), "venue": listed["venue"], "owner": v.get("owner"),
                  "price": price, "fee": fee, "cash": me["cash"], "checks": checks}))
if not all(checks.values()): sys.exit("DENY refused: " + ", ".join(k for k, ok in checks.items() if not ok))
if dry: sys.exit("dry run: all checks pass")
r = b.accept(oid); print(time.strftime("%H:%M:%S"), "ACCEPTED", json.dumps(r)[:300])
