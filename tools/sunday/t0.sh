#!/usr/bin/env bash
# Sunday t+0 (Operator; directive 07:05, contra-ops §3). Deterministic, no Claude prompt needed.
# 08:35 book restart (floor 0) · waits for R (doors open, not paused, tick > 1445) → logs the case → waits for C (CHA released)
# → silver pack (gate) → Pícaros chain CHA-09 → CHA-10 → MAL-09 → MAL-10 (offer-only, trick guard in simple_buy)
# → book merge at C+30 s → R+10 trader/opps/swaps from run/floors.env.
R=/Users/lucaswiese/Documents/claude-hackathon-team-5; set -a; . "$R/.env"; set +a
O="$R/run/sunday"; L="$R/logs/t0.log"; CH="$R/logs/picaros_chain.log"
log() { echo "$(date +%T) $*" >> "$L"; }
j() { curl -s --max-time 5 "$BAZAAR_URL$1"; }                       # keyless reads
k() { curl -s --max-time 8 -H "X-Team-Key: $BAZAAR_KEY" "$BAZAAR_URL$1"; }
hhmm() { date +%H%M | sed 's/^0*//'; }
log "t0 armed (pid $$)"

# --- 08:35-08:38: book on floor 0, swaps/recorder off, opps already off ---
until [ "$(hhmm)" -ge 835 ] 2>/dev/null; do sleep 15; done
( cd "$R" && tools/daemons.sh stop opps swaps recorder >> "$L" 2>&1
  CASH_FLOOR=0 MIN_GAIN_SELL=2 tools/daemons.sh restart book >> "$L" 2>&1 )
sleep 5; log "book.py processes: $(pgrep -f agents/trader/book.py | wc -l | tr -d ' ') · opps/swaps left: $(pgrep -f 'tools/opportunities.py|agents/trader/swaps.py' | wc -l | tr -d ' ')"

# --- R ---
until j /api/clock | python3 -c 'import sys,json;c=json.load(sys.stdin);sys.exit(0 if c.get("tick",0)>1445 and not c.get("paused") else 1)' 2>/dev/null; do sleep 2; done
CASE=$(j /api/clock | python3 -c 'import sys,json;c=json.load(sys.stdin);print(c.get("tick"),"round",c.get("round"),"t_hours",c.get("t_hours") or c.get("now_hours"))' 2>/dev/null)
log "R: $CASE"
RT=$(date +%s)

# --- R+10 restarts in the background (trader, opps RET-only, swaps; 15 s apart) ---
( sleep 600; set -a; . "$R/run/floors.env"; set +a
  cd "$R"
  # trader: HELD unless the Builder's rival-venue skip is on (Chief 07:15, contra-market); flag file run/trader_ok
  if [ -f "$R/run/trader_ok" ]; then CASH_FLOOR=$TRADER_FLOOR tools/daemons.sh restart trader >> "$L" 2>&1; T="trader floor $TRADER_FLOOR"
  else tools/daemons.sh stop trader >> "$L" 2>&1; T="trader HELD (rival-venue skip not confirmed: touch run/trader_ok to allow)"; fi
  sleep 15
  OPPS_BUILD=RET CASH_FLOOR=$OPPS_FLOOR tools/daemons.sh start opps >> "$L" 2>&1; sleep 15
  tools/daemons.sh start swaps >> "$L" 2>&1
  echo "$(date +%T) R+10 restarts done: $T, opps RET floor $OPPS_FLOOR, swaps" >> "$L" ) &

# --- C: CHA released (keyless catalog) ---
until j /api/catalog | python3 -c 'import sys,json;d=json.load(sys.stdin);sys.exit(0 if any(s.get("id")=="CHA" and s.get("released") for s in d.get("sets",[])) else 1)' 2>/dev/null; do sleep 3; done
log "C: CHA released"

# silver pack 1013, gate: open only while >= 2 CHA page cards are still missing
MISS=$(k /api/me | python3 -c 'import sys,json;d=json.load(sys.stdin);h={a["ref"] for a in d["assets"]};print(sum(1 for i in range(1,11) if f"CHA-{i:02d}" not in h))' 2>/dev/null)
if [ "${MISS:-0}" -ge 2 ]; then
  log "pack 1013: CHA missing $MISS → open"; python3 - >> "$L" 2>&1 <<'EOF'
import os,sys,json
sys.path.insert(0,'/Users/lucaswiese/Documents/claude-hackathon-team-5/bazaar-kit')
from bazaar_sdk import Bazaar
b=Bazaar(os.environ['BAZAAR_URL'],os.environ['BAZAAR_KEY'],wait_on_tick=False,timeout=10.0)
try: print('pack opened:', json.dumps(b.open_pack(1013))[:600])
except Exception as e: print('pack open failed:', repr(e)[:200])
EOF
else log "pack 1013 NOT opened (CHA missing ${MISS:-?} < 2)"; fi

# Pícaros chain (background): exact card, offer-only; reopen once on a walk
EGG='Conozco el timo de la estampita, como Lazarillo y Rinconete. Sin trucos, ¿eh? {p} P por la carta.'
held() { k /api/me | python3 -c "import sys,json;d=json.load(sys.stdin);sys.exit(0 if any(a['ref']=='$1' for a in d['assets']) else 1)" 2>/dev/null; }
cash() { k /api/me | python3 -c 'import sys,json;print(json.load(sys.stdin)["cash"])' 2>/dev/null; }
cutoff() { [ "$(hhmm)" -lt "${STOP_HHMM:-1040}" ]; }
B() { python3 -u "$O/simple_buy.py" "$1" --dealer picaros --open "$2" --step 2 --cap "$3" --floor-cash 0 --offer-only --first-text "$EGG" --deadline 420; }
( for c in CHA-09 CHA-10; do
    cutoff || { echo "$(date +%T) cutoff: $c skipped"; continue; }
    held $c && { echo "$(date +%T) $c already held"; continue; }
    B $c 42 54; sleep 20
    held $c || { echo "$(date +%T) $c reopen at cap 57"; B $c 42 57; sleep 20; }
  done
  for c in MAL-09 MAL-10; do
    cutoff || { echo "$(date +%T) cutoff: $c skipped"; continue; }
    held $c && continue
    C=$(cash); if [ "${C:-0}" -lt 373 ]; then echo "$(date +%T) $c skipped: cash $C < 373 (49 + 174 CHA left + 150 MAL gate)"; continue; fi
    B $c 40 49; sleep 20
    held $c || { B $c 40 49; sleep 20; }
  done
  echo "$(date +%T) chain done" ) >> "$CH" 2>&1 &

# book merge at C+30 s (atomic)
sleep 30
if python3 -c "import json;json.load(open('$R/run/book.sunday.json'))" 2>/dev/null; then
  mv "$R/run/book.sunday.json" "$R/run/book.json" && log "book merged (CHA public bids + LAT fodder bids)"
else log "book.sunday.json invalid or missing: NOT merged"; fi
wait
log "t0 done"
