"""Sunday v10 ad (Chief 10:00; text 10:46 deal reward; 11:00 CHA standing bids). One transactional line every 15 min until
15:00 via the starter broker. The bids claim is posted only while v10's board (read keyless) really shows those bids;
otherwise the line without it, so the ad never advertises an expired bid."""
import os, sys, time, json, urllib.request
sys.path.insert(0, "/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit")
from bazaar_sdk import Bazaar, Broker  # noqa: E402
FULL = ("v10 (Puesto de Team 5), 0% fee: standing bids live now for CHA-01, CHA-03 and CHA-05 at 6 P, and they fill in "
        "the same tick. Post your spares on v10. Deal reward: close a trade on v10 and Team 5 buys one of your spare LAT "
        "cards at a fair price.")
BASE = ("v10 (Puesto de Team 5), 0% fee. Post your spares on v10. Deal reward: close a trade on v10 and Team 5 buys one "
        "of your spare LAT cards at a fair price.")
URL = os.environ["BAZAAR_URL"]
b = Bazaar(URL, os.environ["BAZAAR_KEY"], wait_on_tick=False, timeout=10.0)
br = Broker(URL, b.me()["starter_broker_key"])

def bids_live(tries=4):
    """The maker re-posts these bids every few minutes (cancel, then post): retry across the gap."""
    for i in range(tries):
        if _bids_live(): return True
        time.sleep(8)
    return False

def _bids_live():
    try:
        with urllib.request.urlopen(URL + "/api/venues/v10/offers", timeout=8) as r:  # keyless public read
            offers = json.load(r).get("offers", [])
    except Exception:
        return False
    have = {t for o in offers if (o.get("give") or {}).get("cash", 0) >= 6 for t in (o.get("want") or {}).get("types") or []}
    return {"card:CHA-01", "card:CHA-03", "card:CHA-05"} <= have

time.sleep(float(sys.argv[1]) if len(sys.argv) > 1 else 0)  # optional start delay (1 announcement per 20 ticks)
while time.strftime("%H%M") < "1500":
    text = FULL if bids_live() else BASE
    try:
        print(time.strftime("%H:%M:%S"), "ANNOUNCE", "full" if text is FULL else "base", br.announce(text), flush=True)
    except Exception as e:  # noqa: BLE001
        print(time.strftime("%H:%M:%S"), "ERR", repr(e)[:150], flush=True); time.sleep(60); continue
    time.sleep(900)
