"""v10 deal reward (GUARDRAIL, Lucas's call via the Chief 10:45). For every trade the feed settles ON v10 (between two other
teams: we cannot trade on our own venue), buy ONE spare card from one of its parties that we LACK, at price <= our
/api/me/value (a >= 0 deal for us, never a gift), <= 10 P each, <= 100 P in all (open + filled), on a member's 0% market
(v21; v05 if the party is t09), never v10 or v24 and never the party's own venue. Each buy is logged with its v10 settlement id.
LAT first copies only: MAL-07/09 stay with mal_close.py (never two live MAL bids). Holdings are evidence from the feed
(settlement items, offer.listed gives). Counterparty passes policy.check (no rivals), never t10; at most 2 rewards per team
(a cap against two teams farming it with empty trades). One addressed bid per reward, 120 ticks, not re-posted.

BOUNTY (GUARDRAIL 11:25, Lucas's explicit call; the Chief flagged the fair-play review risk): the FIRST 3 trades settled
on v10 between two other teams (any team except t10), max 1 per seller, pay the SELLER a 10 P bonus: one addressed
want-card bid to the seller for a card the feed shows it holds, at our value + 10 (max 10 P over value), on v21 (v05 if
the seller is t09). Prefer a LAT first copy we lack; otherwise any card, most recently seen first. MAL-07/09 are left out
(mal_close.py owns them: never two live MAL bids). Each bounty is logged with its v10 settlement id. Later trades get
the LAT reward above."""
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
st.setdefault("bounties", []); st.setdefault("bounty_trades", [])
BOUNTIES, BONUS = 3, 10
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

seen_at = {}   # asset id -> feed id of the latest evidence (recency for the bounty's fallback card)
_learn = learn
def learn(e):
    _learn(e)
    p = e.get('payload') or {}
    ids = [it['id'] for it in p.get('items') or [] if it.get('kind') == 'card'] if e['type'] == 'settlement' else \
          [a['id'] for a in ((p.get('offer') or {}).get('give') or {}).get('assets') or [] if a.get('kind') == 'card'] if e['type'] == 'offer.listed' else []
    for i in ids: seen_at[i] = e.get('id', 0)

def holds(team):
    return {ref for t, ref in owner.values() if t == team}

def holds_recent(team):
    """Refs the feed shows `team` holding, most recent evidence first."""
    out = []
    for i in sorted((i for i, (t, r) in owner.items() if t == team), key=lambda i: -seen_at.get(i, 0)):
        if owner[i][1] not in out: out.append(owner[i][1])
    return out

def seller_of(p):
    cards = [it for it in p.get('items') or [] if it.get('kind') == 'card']
    return cards[0].get('frm') if cards else None

def bounty_eligible(p):
    parties = [t for t in p.get('parties') or [] if t]
    if len(parties) != 2 or not all(t.startswith('t') for t in parties) or 't05' in parties or 't10' in parties: return False
    s = seller_of(p)
    return bool(s) and len(st['bounty_trades']) < BOUNTIES and all(x['seller'] != s for x in st['bounties'])

def bounty(e):
    p = e['payload']; sid = p['settlement']; s = seller_of(p)
    st['bounty_trades'].append(sid); st['done'].append(sid); save()
    held = {a['ref'] for a in retry(b.me)['assets']}
    recent = [c for c in holds_recent(s) if not c.startswith('MAL-')]
    pick = next((c for c in recent if c in WANT and c not in held), None) or (recent[0] if recent else None)
    if not pick:
        st['bounties'].append({"settlement": sid, "seller": s, "card": None, "price": 0, "offer": None}); save()
        log(event="bounty_skip", settlement=sid, seller=s, why="no card of the seller's known from the feed"); return
    v = float(retry(b.value, pick)['your_value']); price = int(v) + BONUS
    venue = 'v05' if s == 't09' else 'v21'
    r = retry(b.list_offer, give={"cash": price}, want={"types": [f"card:{pick}"]}, venue=venue, to=s, expires_in_ticks=120)
    st['bounties'].append({"settlement": sid, "seller": s, "card": pick, "price": price, "value": v, "offer": r.get('id'), "venue": venue}); save()
    log(event="bounty", n=len(st['bounty_trades']), settlement=sid, seller=s, card=pick, price=price, value=v,
        lacked=pick in WANT and pick not in held, venue=venue, offer=r.get('id'), exp=r.get('expires_tick'))

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
            try: bounty(e) if bounty_eligible(p) else reward(e)
            except Exception as ex: log(event="error", settlement=p.get('settlement'), err=repr(ex)[:200])
    time.sleep(5)
log(event="end", why="14:00 cutoff (new dealer/thread cut; rewards stop)")
