"""Chief 13:30 (Lucas): MAL-09 bids on v01 (Team 6's market), ONE live at a time, always ADDRESSED, give 60, 40 ticks:
27446 → t01 (live) → on lapse t09 → then t15; stop when one fills or after t15. Never t04/t10/t12/t13/t17/t18.
Counter: if t01/t09/t15 lists MAL-09 to us on v01 at <= 75, cancel our bid first, then accept it."""
import os, sys, json, time
sys.path.insert(0, '/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit')
from bazaar_sdk import Bazaar
b = Bazaar(os.environ['BAZAAR_URL'], os.environ['BAZAAR_KEY'], wait_on_tick=False, timeout=10.0)
F = '/Users/lucaswiese/Documents/claude-hackathon-team-5/data/feed.jsonl'
QUEUE, OK, PRICE, LIFE, MAXC = ["t09", "t15"], {"t01", "t09", "t15"}, 60, 40, 75
def log(**kw): print(json.dumps({"t": time.strftime('%H:%M:%S'), **kw}), flush=True)
def held(): return any(a['ref'] == 'MAL-09' for a in b.me()['assets'])
def ours(): return [o for o in b.my_offers().get('offers', []) if o.get('status') == 'open' and o.get('maker') == 't05'
                    and 'card:MAL-09' in ((o.get('want') or {}).get('types') or [])]
pos = os.path.getsize(F); log(event="start", live=[o['id'] for o in ours()], queue=QUEUE)
while time.strftime('%H%M') < '1455':
    try:
        with open(F) as f: f.seek(pos); chunk = f.read(); pos = f.tell()
        for line in chunk.splitlines():
            try: e = json.loads(line)
            except Exception: continue
            o = (e.get('payload') or {}).get('offer') or {}
            if e['type'] != 'offer.listed' or e.get('actor') not in OK or o.get('venue') != 'v01' or o.get('to') != 't05': continue
            if not any(a.get('ref') == 'MAL-09' for a in (o.get('give') or {}).get('assets') or []): continue
            price = (o.get('want') or {}).get('cash', 0); log(event="counter", by=e['actor'], offer=o.get('id'), price=price)
            if price > MAXC: log(event="ignore", offer=o.get('id'), why="> 75"); continue
            for x in ours(): b.cancel(x['id']); log(event="closed", offer=x['id'], why="counter <= 75 replaces it")
            time.sleep(1)
            if held(): log(event="end", why="our bid filled first"); sys.exit()
            for i in range(6):
                try: log(event="accept", offer=o['id'], result=json.dumps(b.accept(o['id']))[:200]); break
                except Exception as ex: log(event="accept_retry", i=i, err=repr(ex)[:120]); time.sleep(6)
            time.sleep(20); log(event="end", held=held(), neg=b.me()['score'].get('neg_points')); sys.exit()
        if held(): log(event="end", why="MAL-09 ours: MAL PAGE COMPLETE", neg=b.me()['score'].get('neg_points')); break
        if not ours():
            if not QUEUE: log(event="end", why="t01, t09 and t15 bids lapsed unfilled"); break
            to = QUEUE.pop(0)
            r = b.list_offer(give={"cash": PRICE}, want={"types": ["card:MAL-09"]}, venue="v01", to=to, expires_in_ticks=LIFE)
            log(event="open", card="MAL-09", to=to, venue="v01", price=PRICE, offer=r.get('id'), exp=r.get('expires_tick'))
    except Exception as ex:
        log(event="error", err=repr(ex)[:150])
    time.sleep(10)
