"""v10 deal reward (GUARDRAIL, Lucas's call via the Chief 10:45). For every trade the feed settles ON v10 (between two other
teams: we cannot trade on our own venue), buy ONE spare card from one of its parties that we LACK, at price <= our
/api/me/value (a >= 0 deal for us, never a gift), <= 10 P each, <= 100 P in all (open + filled), on a member's 0% market
(v21; v05 if the party is t09), never v10 or v24 and never the party's own venue. Each buy is logged with its v10 settlement id.
LAT first copies only: MAL-07/09 stay with mal_close.py (never two live MAL bids). Holdings are evidence from the feed
(settlement items, offer.listed gives). Counterparty passes policy.check (no rivals), never t10; at most 2 rewards per team
(a cap against two teams farming it with empty trades). One addressed bid per reward, 120 ticks, not re-posted."""
import os, sys, json, time
ROOT = '/Users/lucaswiese/Documents/claude-hackathon-team-5'
sys.path.insert(0, ROOT + '/bazaar-kit'); sys.path.insert(0, ROOT + '/tools')
from bazaar_sdk import Bazaar
import policy
b = Bazaar(os.environ['BAZAAR_URL'], os.environ['BAZAAR_KEY'], wait_on_tick=False, timeout=10.0)
FEED, STATE = ROOT + '/data/feed.jsonl', ROOT + '/run/v10_reward.json'
EACH, TOTAL, PER_TEAM = 10, 100, 2
WANT = [f"LAT-{i:02d}" for i in range(1, 11)]

def log(**kw):
    print(json.dumps({"t": time.strftime('%H:%M:%S'), **kw}), flush=True)

def retry(f, *a, **kw):
    for i in range(4):
        try: return f(*a, **kw)
        except Exception as e: err = e; time.sleep(3)
    raise err

try: st = json.load(open(STATE))
except Exception: st = {"done": [], "bids": []}   # bids: {settlement, team, card, price, offer, venue}
def save():
    json.dump(st, open(STATE + '.tmp', 'w'), indent=1); os.replace(STATE + '.tmp', STATE)

owner = {}   # asset id -> (team, ref), from the feed
def learn(e):
    p = e.get('payload') or {}
    if e['type'] == 'settlement':
        for it in p.get('items') or []:
            if it.get('kind') == 'card': owner[it['id']] = (it.get('to'), it.get('ref'))
    elif e['type'] == 'offer.listed':
        o = p.get('offer') or {}
        for a in (o.get('give') or {}).get('assets') or []:
            if a.get('kind') == 'card' and o.get('maker', '').startswith('t'): owner[a['id']] = (o['maker'], a.get('ref'))

def holds(team):
    return {ref for t, ref in owner.values() if t == team}

def committed():
    """P in reward bids that are open or filled (an expired/cancelled one releases its budget)."""
    mine = {o['id']: o for o in retry(b.my_offers).get('offers', [])}
    held = {a['ref'] for a in retry(b.me)['assets']}
    tot = 0
    for x in st['bids']:
        o = mine.get(x['offer'])
        if (o and o.get('status') == 'open') or x['card'] in held or x.get('filled'): tot += x['price']
    return tot

def reward(e):
    p = e['payload']; sid = p['settlement']
    if sid in st['done']: return
    st['done'].append(sid); save()
    parties = [t for t in p.get('parties') or [] if t and t.startswith('t') and t != 't05']
    teams = retry(b.leaderboard).get('teams') or []
    held = {a['ref'] for a in retry(b.me)['assets']}
    mine = {o['id']: o for o in retry(b.my_offers).get('offers', [])}
    bidding = {x['card'] for x in st['bids'] if (mine.get(x['offer']) or {}).get('status') == 'open'}
    lack = [c for c in WANT if c not in held and c not in bidding]
    budget = TOTAL - committed()
    if budget < 1: log(event="skip", settlement=sid, why="100 P budget used"); return
    for team in parties:
        if team == 't10': continue
        if sum(x['team'] == team for x in st['bids']) >= PER_TEAM: log(event="skip", settlement=sid, team=team, why="2 rewards already"); continue
        cands = [c for c in lack if c in holds(team)]
        best = None
        for c in cands:
            v = float(retry(b.value, c)['your_value']); price = min(EACH, int(v), budget)
            if price >= 1 and (best is None or price > best[2]): best = (c, v, price)
        if not best: log(event="skip", settlement=sid, team=team, why=f"no known spare LAT we lack (seen {sorted(holds(team) & set(WANT))})"); continue
        c, v, price = best
        ok, why = policy.check(team, teams=teams, our_gain=v - price, their_gain=None)
        if not ok: log(event="skip", settlement=sid, team=team, card=c, why=why); continue
        venue = 'v05' if team == 't09' else 'v21'
        r = retry(b.list_offer, give={"cash": price}, want={"types": [f"card:{c}"]}, venue=venue, to=team, expires_in_ticks=120)
        st['bids'].append({"settlement": sid, "team": team, "card": c, "price": price, "value": v, "offer": r.get('id'), "venue": venue}); save()
        log(event="open", settlement=sid, team=team, card=c, price=price, value=v, venue=venue, offer=r.get('id'), exp=r.get('expires_tick'))
        return
    log(event="skip", settlement=sid, parties=parties, why="no eligible party/card")

pos = 0
with open(FEED) as f:
    for line in f:
        try: learn(json.loads(line))
        except Exception: pass
    pos = f.tell()
log(event="start", known_assets=len(owner), done=len(st['done']), bids=len(st['bids']))
while time.strftime('%H%M') < '1400':
    with open(FEED) as f:
        f.seek(pos); chunk = f.read(); pos = f.tell()
    for line in chunk.splitlines():
        try: e = json.loads(line)
        except Exception: continue
        learn(e)
        p = e.get('payload') or {}
        if e['type'] == 'settlement' and p.get('venue') == 'v10' and p.get('kind') == 'trade':
            log(event="v10_trade", settlement=p.get('settlement'), parties=p.get('parties'), items=[i.get('ref') for i in p.get('items') or []], price=p.get('price'))
            try: reward(e)
            except Exception as ex: log(event="error", settlement=p.get('settlement'), err=repr(ex)[:200])
    time.sleep(5)
log(event="end", why="14:00 cutoff (new dealer/thread cut; rewards stop)")
