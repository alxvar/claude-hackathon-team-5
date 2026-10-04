"""Ladder fodder (Chief 11:50): when the book's El Rastro bids (LAT-06/07/08 at 9) fill, sell that uncommon to a dealer
above its opening and above our value (12.5): Pilar > 16 for the empty 3rd L3 slot first, then Chato > 13 for our
empty L2 slots (3). Each card copy gets one try per dealer: Pilar, then Chato if she walks; a copy both walk on is kept.
Stops after 1 Pilar + 3 Chato deals (new slots only) or at 14:00 (new dealer threads cut)."""
import os, sys, json, time, subprocess
ROOT = '/Users/lucaswiese/Documents/claude-hackathon-team-5'
sys.path.insert(0, ROOT + '/bazaar-kit')
from bazaar_sdk import Bazaar
b = Bazaar(os.environ['BAZAAR_URL'], os.environ['BAZAAR_KEY'], wait_on_tick=False, timeout=10.0)
STATE = ROOT + '/run/lat_fodder.json'
CARDS = ("LAT-06", "LAT-07", "LAT-08")
PLAN = [("pilar", 24, 17, 1), ("chato", 20, 14, 3)]   # dealer, ask, floor (> opening checked by dealer_sell), slots

def log(**kw):
    print(json.dumps({"t": time.strftime('%H:%M:%S'), **kw}), flush=True)

try: st = json.load(open(STATE))
except Exception: st = {"deals": {"pilar": 0, "chato": 0}, "tried": {}}   # tried: asset id -> [dealers]
def save():
    json.dump(st, open(STATE + '.tmp', 'w'), indent=1); os.replace(STATE + '.tmp', STATE)

def sell(card, dealer, ask, floor):
    out = subprocess.run([sys.executable, '-u', ROOT + '/run/sunday/dealer_sell.py', card, '--dealer', dealer, '--ask', str(ask),
                          '--step', '1', '--floor', str(floor)], capture_output=True, text=True, timeout=900).stdout
    end = [json.loads(l) for l in out.splitlines() if l.startswith('{') and '"event": "end"' in l]
    return end[-1] if end else {"status": "no_end", "tail": out[-300:]}

log(event="start", state=st)
while time.strftime('%H%M') < '1400':
    if all(st['deals'][d] >= n for d, _, _, n in PLAN): log(event="end", why="all new ladder slots used"); break
    try: assets = [a for a in b.me()['assets'] if a['ref'] in CARDS]
    except Exception as e: log(event="error", where="me", err=repr(e)[:120]); time.sleep(30); continue
    for a in assets:
        tried = st['tried'].setdefault(str(a['id']), [])
        for dealer, ask, floor, slots in PLAN:
            if dealer in tried or st['deals'][dealer] >= slots: continue
            tried.append(dealer); save()
            log(event="open", card=a['ref'], asset=a['id'], dealer=dealer, ask=ask, floor=floor)
            r = sell(a['ref'], dealer, ask, floor)
            log(event="result", card=a['ref'], dealer=dealer, status=r.get('status'), ours=r.get('ours'), first=r.get('first'),
                before=r.get('before'), after=r.get('after'))
            if r.get('status') == 'deal':
                st['deals'][dealer] += 1; save(); break
            time.sleep(20)
        time.sleep(5)
    time.sleep(30)
