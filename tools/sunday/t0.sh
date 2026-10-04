#!/usr/bin/env bash
# Sunday t+0 (Operator owns it; directives 07:05 + 07:25 contra-cha). Deterministic, no Claude prompt needed.
# 08:35 book floor 0 · R (doors open, not paused, tick > 1445): case log · R+10 trader(if trader_ok)/opps(RET)/swaps
# C (CHA released): pack gate · Workshop (LAV-02 ×2 + LAV-03) · Pícaros chain CHA-09 → CHA-10 (≤ 57 → 60 → 62 after a
# logged walk; Chato ≤ 100 fallback on no stock) → LAV-04 sell (L4 slot) · Abuela commons CHA-01..03 from C+5 ·
# C+30 s book merge (no CHA-09/10 public) · C+45 Abuela uncommons CHA-06/07 + CHA-04 · C+60 public rare bids only if
# a rare is still missing · watcher: drop our public bid for any CHA card t10/t01 obtains. MAL is NOT in this job.
R=/Users/lucaswiese/Documents/claude-hackathon-team-5; set -a; . "$R/.env"; set +a
O="$R/run/sunday"; L="$R/logs/t0.log"; CH="$R/logs/picaros_chain.log"; AB="$R/logs/abuela_chain.log"
log() { echo "$(date +%T) $*" >> "$L"; }
j() { curl -s --max-time 5 "$BAZAAR_URL$1"; }                       # keyless reads
k() { curl -s --max-time 8 -H "X-Team-Key: $BAZAAR_KEY" "$BAZAAR_URL$1"; }
hhmm() { date +%H%M | sed 's/^0*//'; }
held() { k /api/me | python3 -c "import sys,json;d=json.load(sys.stdin);sys.exit(0 if any(a['ref']=='$1' for a in d['assets']) else 1)" 2>/dev/null; }
cutoff() { [ "$(hhmm)" -lt "${STOP_HHMM:-1340}" ]; }                # dealers close ≈ 14:00 (warning 13:48)
walked() { tail -n 60 "$1" | grep -q '"event": "walk"'; }
# pending(CARD): an open offer of ours wanting CARD, or an open thread with picaros/chato/abuela (a deal may still settle)
pending() { k /api/me/offers | python3 -c "import sys,json;d=json.load(sys.stdin);sys.exit(0 if any(o.get('status')=='open' and o.get('maker')=='t05' and ('card:$1' in ((o.get('want') or {}).get('types') or []) or any(x.get('ref')=='$1' for x in ((o.get('want') or {}).get('assets') or []))) for o in d.get('offers',[])) else 1)" 2>/dev/null && return 0
            k /api/me/threads | python3 -c "import sys,json;d=json.load(sys.stdin);sys.exit(0 if any(t.get('status')=='open' and t.get('with') in ('picaros','chato','abuela') for t in d.get('threads',[])) else 1)" 2>/dev/null; }
settled_or_free() { sleep 35; held "$1" && return 1; pending "$1" && { sleep 35; held "$1" && return 1; pending "$1" && return 1; }; return 0; }  # 0 = free to try another source
log "t0 armed (pid $$)"

# --- 08:35: book on floor 0, swaps/recorder/opps off ---
until [ "$(hhmm)" -ge 835 ] 2>/dev/null; do sleep 15; done
( cd "$R" && tools/daemons.sh stop opps swaps recorder >> "$L" 2>&1
  CASH_FLOOR=0 MIN_GAIN_SELL=2 tools/daemons.sh restart book >> "$L" 2>&1 )
sleep 5; log "08:35 book.py: $(pgrep -f agents/trader/book.py | wc -l | tr -d ' ') process(es) · HEAD $(cd "$R" && git rev-parse --short HEAD)"

# --- R ---
until j /api/clock | python3 -c 'import sys,json;c=json.load(sys.stdin);sys.exit(0 if c.get("tick",0)>1445 and not c.get("paused") else 1)' 2>/dev/null; do sleep 2; done
log "R: $(j /api/clock | python3 -c 'import sys,json;c=json.load(sys.stdin);print(c.get("tick"),"round",c.get("round"),"t_hours",c.get("t_hours") or c.get("now_hours"))' 2>/dev/null)"

( sleep 600; set -a; . "$R/run/floors.env"; set +a; cd "$R"
  if [ -f "$R/run/trader_ok" ]; then CASH_FLOOR=$TRADER_FLOOR tools/daemons.sh restart trader >> "$L" 2>&1; T="trader floor $TRADER_FLOOR (HEAD $(git rev-parse --short HEAD))"
  else tools/daemons.sh stop trader >> "$L" 2>&1; T="trader HELD (no run/trader_ok)"; fi
  sleep 15; OPPS_BUILD=RET CASH_FLOOR=$OPPS_FLOOR tools/daemons.sh start opps >> "$L" 2>&1
  sleep 15; tools/daemons.sh start swaps >> "$L" 2>&1
  echo "$(date +%T) R+10 restarts: $T, opps RET floor $OPPS_FLOOR, swaps" >> "$L" ) &

# --- C ---
until j /api/catalog | python3 -c 'import sys,json;d=json.load(sys.stdin);sys.exit(0 if any(s.get("id")=="CHA" and s.get("released") for s in d.get("sets",[])) else 1)' 2>/dev/null; do sleep 3; done
log "C: CHA released"; CT=$(date +%s)

# pack 1013 (gate: >= 2 CHA page cards missing) + Workshop LAV-02 ×2 + LAV-03 (spares only, can-give YES each)
python3 - >> "$L" 2>&1 <<'EOF'
import os,sys,json,subprocess
ROOT='/Users/lucaswiese/Documents/claude-hackathon-team-5'
sys.path.insert(0,ROOT+'/bazaar-kit'); sys.path.insert(0,ROOT+'/tools')
from bazaar_sdk import Bazaar
import policy
b=Bazaar(os.environ['BAZAAR_URL'],os.environ['BAZAAR_KEY'],wait_on_tick=False,timeout=10.0)
me=b.me(); held={a['ref'] for a in me['assets']}
miss=sum(1 for i in range(1,11) if f"CHA-{i:02d}" not in held)
if miss>=2 and any(a['id']==1013 for a in me['assets']):
    try: print('pack 1013 opened:', json.dumps(b.open_pack(1013))[:500])
    except Exception as e: print('pack open failed:', repr(e)[:200])
else: print(f'pack 1013 not opened (CHA missing {miss})')
# Workshop: pick 3 spare commons among LAV-02/LAV-03, never a page's last free copy
me=b.me(); offs=b.my_offers().get('offers',[]); gone=policy.committed(offs, me['id'])
pick=[]
for ref,n in (('LAV-02',2),('LAV-03',1)):
    for _ in range(n):
        free=[a for a in me['assets'] if a['ref']==ref and a['id'] not in gone and a['id'] not in pick]
        if len(free)<2: break                      # keep >= 1 copy (complete LAV page)
        a=free[-1]
        if policy.last_copy(me, ref, committed_ids=gone|set(pick), giving={a['id']}): break
        pick.append(a['id'])
if len(pick)==3:
    try: print('Workshop', pick, '→', json.dumps(b._call('POST','/api/taller',{'assets':pick}))[:400])
    except Exception as e: print('Workshop failed:', repr(e)[:200])
else: print('Workshop skipped: only', len(pick), 'free LAV spares', pick)
EOF

EGG='Conozco el timo de la estampita, como Lazarillo y Rinconete. Sin trucos, ¿eh? {p} P por la carta.'
P() { python3 -u "$O/simple_buy.py" "$1" --dealer picaros --open 42 --step 2 --cap "$2" --floor-cash 0 --offer-only --first-text "$EGG" --base-value 112 --deadline 420; }

# Pícaros chain (background): CHA-09 → CHA-10 at ≤ 57, then ≤ 60, then ≤ 62 (reopen only after a logged walk); no stock → Chato ≤ 100
( for c in CHA-09 CHA-10; do
    cutoff || { echo "$(date +%T) cutoff: $c skipped"; continue; }
    held $c && { echo "$(date +%T) $c already held"; continue; }
    for cap in 57 60 62; do
      P $c $cap > "$CH.$c.$cap" 2>&1; cat "$CH.$c.$cap"
      settled_or_free $c || { echo "$(date +%T) $c held or a deal pending after cap $cap: no further source"; break; }
      walked "$CH.$c.$cap" && continue                     # a logged walk → next tier
      echo "$(date +%T) $c: no logged walk at cap $cap (no stock/timeout/trick), not held, nothing pending → Chato ≤ 100"
      python3 -u "$O/simple_buy.py" $c --dealer chato --open 60 --step 3 --cap 100 --floor-cash 0 --offer-only --base-value 112 --deadline 480
      settled_or_free $c >/dev/null; break
    done
  done
  # LAV-04 spare → Pícaros (L4 slot), floor 5 (above their opening 4)
  if cutoff && (cd "$R" && python3 tools/policy.py can-give LAV-04 | grep -q '^YES'); then
    python3 -u "$O/dealer_sell.py" LAV-04 --dealer picaros --ask 12 --step 1 --floor 5; fi
  echo "$(date +%T) Pícaros chain done" ) >> "$CH" 2>&1 &

# Abuela commons CHA-01..03 from C+5 (parallel; one Abuela thread at a time), then C+45 uncommons + CHA-04
A() { python3 -u "$O/simple_buy.py" "$1" --dealer abuela --open "$2" --step 1 --cap "$3" --floor-cash 0 --offer-only --base-value "$4" --deadline 420; }
( sleep 300
  for c in CHA-01 CHA-02 CHA-03; do cutoff && ! held $c && { A $c 5 9 16; sleep 15; }; done
  while [ $(( $(date +%s) - CT )) -lt 2700 ]; do sleep 20; done      # C+45
  for c in CHA-06 CHA-07; do cutoff && ! held $c && { A $c 12 22 40; sleep 15; }; done
  cutoff && ! held CHA-04 && A CHA-04 5 9 16
  echo "$(date +%T) Abuela chain done" ) >> "$AB" 2>&1 &

# book merge at C+30 s (atomic): public CHA-01..08 capped + LAT fodder; no CHA-09/10, no LAV asks
sleep 30
if python3 -c "import json;json.load(open('$R/run/book.sunday.json'))" 2>/dev/null; then
  mv "$R/run/book.sunday.json" "$R/run/book.json" && log "book merged (public CHA-01..08 capped + LAT fodder)"
else log "book.sunday.json invalid or missing: NOT merged"; fi

# watcher: drop our public bid for any CHA card t10/t01 obtains (feed: dealer settlements, pack best, Workshop); C+60 rares
python3 - >> "$L" 2>&1 <<'EOF' &
import os,sys,json,time,re
ROOT='/Users/lucaswiese/Documents/claude-hackathon-team-5'; F=ROOT+'/data/feed.jsonl'; B=ROOT+'/run/book.json'
sys.path.insert(0,ROOT+'/bazaar-kit')
from bazaar_sdk import Bazaar
b=Bazaar(os.environ['BAZAAR_URL'],os.environ['BAZAAR_KEY'],wait_on_tick=False,timeout=10.0)
WATCH={'t10','t01'}; pos=os.path.getsize(F); t0=time.time(); rares_done=False
def drop(card, why):
    bk=json.load(open(B)); n=len(bk['offers'])
    bk['offers']=[e for e in bk['offers'] if not (e['card']==card and e['side']=='buy')]
    if len(bk['offers'])<n:
        json.dump(bk,open(B+'.tmp','w'),indent=1); os.replace(B+'.tmp',B); print(time.strftime('%H:%M:%S'),'watcher: dropped public bid',card,'—',why,flush=True)
while time.strftime('%H%M')<'1400':
    with open(F) as f: f.seek(pos); chunk=f.read(); pos=f.tell()
    for line in chunk.splitlines():
        if 'CHA-' not in line: continue
        try: e=json.loads(line)
        except Exception: continue
        p=e.get('payload') or {}
        if e.get('type')=='settlement':
            for it in p.get('items') or []:
                if str(it.get('ref','')).startswith('CHA-') and it.get('to') in WATCH: drop(it['ref'], f"{it['to']} got it (settlement {p.get('settlement')})")
        if e.get('type')=='pack.opened' and p.get('team') in WATCH:
            r=(p.get('best') or {}).get('ref','')
            if r.startswith('CHA-'): drop(r, f"{p['team']} pulled it (pack best)")
    if not rares_done and time.time()-t0>3570:          # ≈ C+60 (watcher starts at C+30 s): post public rare bids only if a rare is still missing
        rares_done=True
        held={a['ref'] for a in b.me()['assets']}
        bk=json.load(open(B)); have={e['card'] for e in bk['offers']}
        add=[{"card":c,"side":"buy","price":48,"floor":54,"step":2,"page_closer":True,"life":20} for c in ('CHA-09','CHA-10') if c not in held and c not in have]
        if add:
            bk['offers']+=add; json.dump(bk,open(B+'.tmp','w'),indent=1); os.replace(B+'.tmp',B); print(time.strftime('%H:%M:%S'),'C+60: public rare bids added',[a['card'] for a in add],flush=True)
    time.sleep(20)
EOF
wait
log "t0 done"
