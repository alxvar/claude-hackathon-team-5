"""v10 deal reward (GUARDRAIL, Lucas's call via the Chief 10:45). For every trade the feed settles ON v10 (between two other
teams: we cannot trade on our own venue), buy ONE spare card from one of its parties that we LACK, at price <= our
/api/me/value (a >= 0 deal for us, never a gift), <= 10 P each, <= 100 P in all (open + filled), on EL RASTRO as maker
(Chief 11:33: our own trades must add no VC to other teams' venues; the taker pays El Rastro's fee). Each buy is logged with its v10 settlement id.
LAT first copies only: MAL-07/09 stay with mal_close.py (never two live MAL bids). Holdings are evidence from the feed
(settlement items, offer.listed gives). Counterparty passes policy.check (no rivals), never t10; at most 2 rewards per team
(a cap against two teams farming it with empty trades). One addressed bid per reward, 120 ticks, not re-posted.

BOUNTY (GUARDRAIL 11:38, Lucas: "spend big to get trades on v10"; the Chief flagged the fair-play review risk): the FIRST
5 trades settled on v10 between two other teams (any team except t10), max 2 per seller, pay the SELLER ~20 P, on EL
RASTRO as maker. In kind first (0 cost to our score): buy cards the seller holds (feed evidence) that we LACK (LAT first
copies, MAL-07/09) at <= our value: one card worth >= 20, else up to 3 lacked cards whose values sum to >= 20 (one
offer wanting all of them). Only if that falls short: top up to 20 with cash over value, or any card the seller holds at
value + up to 20. The SUM of (price - our value) over all bounties <= 29 P (our slack under the round cap of 50:
uncapped ~79). Never two of our addressed bids live for the same card. Each bounty logged with its v10 settlement id.
Later trades get the LAT reward above."""
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
BOUNTIES, BONUS, PER_SELLER, SLACK = 5, 20, 2, 0   # Chief 12:20: in kind only (no round cap: overpay costs real neg points)
st.setdefault("over_used", 0.0)
LACK_ALSO = ["MAL-07", "MAL-09"]
STICKY_RIVALS = {"t03", "t06", "t10", "t12", "t13", "t17", "t18"}
LOCKED = {"t10", "t12", "t18", "t03", "t04"}   # Chief 12:33: the reward is non-rivals only (live + this list)
BOOK = ROOT + '/run/book.json'

def all_bid_cards():
    """Cards any open offer of ours wants (the book's public bids included): never a second bid on one card."""
    return {t[5:] for o in retry(b.my_offers).get('offers', []) if o.get('status') == 'open' and o.get('maker') == 't05'
            for t in (o.get('want') or {}).get('types') or [] if t.startswith('card:')}

def take_from_book(cards):
    """A bounty bid replaces the book's public bid for the same card: drop it from run/book.json, cancel the live one."""
    try:
        bk = json.load(open(BOOK)); n = len(bk['offers'])
        bk['offers'] = [e for e in bk['offers'] if not (e['card'] in cards and e['side'] == 'buy')]
        if len(bk['offers']) != n: json.dump(bk, open(BOOK + '.tmp', 'w'), indent=1); os.replace(BOOK + '.tmp', BOOK)
        for o in retry(b.my_offers).get('offers', []):
            if o.get('status') == 'open' and o.get('maker') == 't05' and not o.get('to') and \
                    any(f'card:{c}' in ((o.get('want') or {}).get('types') or []) for c in cards):
                retry(b.cancel, o['id']); log(event="book_handoff", offer=o['id'], cards=cards)
    except Exception as e:
        log(event="error", where="take_from_book", err=repr(e)[:150])
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
    if s in LOCKED: return False   # Chief 13:05 LOCK THE LEAD: zero trades with t10/t12/t18/t03/t04
    return bool(s) and len(st['bounty_trades']) < BOUNTIES and sum(x['seller'] == s for x in st['bounties']) < PER_SELLER

def bounty(e):
    p = e['payload']; sid = p['settlement']; s = seller_of(p)
    st['bounty_trades'].append(sid); st['done'].append(sid); save()
    held = {a['ref'] for a in retry(b.me)['assets']}
    mine = [o for o in retry(b.my_offers).get('offers', []) if o.get('status') == 'open' and o.get('to')]
    addressed = {t[5:] for o in mine for t in (o.get('want') or {}).get('types') or [] if t.startswith('card:')}
    recent = [c for c in holds_recent(s) if c not in addressed]
    val = {}
    def v(c):
        if c not in val: val[c] = float(retry(b.value, c)['your_value'])
        return val[c]
    lacked = sorted((c for c in recent if (c in WANT or c in LACK_ALSO) and c not in held), key=lambda c: -v(c))
    slack = max(0.0, SLACK - st['over_used'])
    pick, over = None, 0
    big = [c for c in lacked if v(c) >= BONUS]
    if big:
        pick = [big[-1]]                                   # the cheapest single lacked card worth >= 20
    elif lacked:
        bundle, tot = [], 0.0
        for c in lacked:
            if len(bundle) < 3: bundle.append(c); tot += v(c)
            if tot >= BONUS: break
        pick = bundle
        if tot < BONUS: over = min(BONUS - int(tot), int(slack))
    elif recent and slack >= 1:
        pick, over = [recent[0]], min(BONUS, int(slack))
    if not pick:
        st['bounties'].append({"settlement": sid, "seller": s, "cards": [], "price": 0, "offer": None}); save()
        log(event="bounty_skip", settlement=sid, seller=s, why=f"no card of the seller's known (or slack {slack:g} used up)"); return
    value = sum(v(c) for c in pick); price = int(value) + over
    take_from_book([c for c in pick if c in all_bid_cards()])
    r = retry(b.list_offer, give={"cash": price}, want={"types": [f"card:{c}" for c in pick]}, venue='rastro', to=s, expires_in_ticks=120)
    st['over_used'] = st['over_used'] + max(0.0, price - value)
    st['bounties'].append({"settlement": sid, "seller": s, "cards": pick, "price": price, "value": value, "over": max(0.0, price - value),
                           "offer": r.get('id'), "venue": 'rastro'}); save()
    log(event="bounty", n=len(st['bounty_trades']), settlement=sid, seller=s, cards=pick, price=price, value=value,
        over=round(max(0.0, price - value), 2), over_used=round(st['over_used'], 2), in_kind=over == 0 and all(c in lacked for c in pick),
        venue='rastro', offer=r.get('id'), exp=r.get('expires_tick'))

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
    bidding = {x['card'] for x in st['bids'] if (mine.get(x['offer']) or {}).get('status') == 'open'} | all_bid_cards()
    lack = [c for c in WANT if c not in held and c not in bidding]
    budget = TOTAL - committed()
    if budget < 1: log(event="skip", settlement=sid, why="100 P budget used"); return
    for team in parties:
        if team == 't10' or team in STICKY_RIVALS or team in policy.rivals(teams) or team in policy.RIVALS:
            log(event="skip", settlement=sid, team=team, why="rival (live policy.rivals, RIVALS or the Chief's list)"); continue
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
        venue = 'rastro'  # Chief 11:33: our trades add no VC to other venues; maker pays no fee
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
