#!/usr/bin/env bash
# Sunday's duelist in one command (Chief, Sun 01:30; for Aleks). Run it from your normal checkout, no merge needed:
#   bash <(git show origin/duelist-loop:tools/duelist_sunday.sh)              # start
#   bash <(git show origin/duelist-loop:tools/duelist_sunday.sh) --rollback   # back to Saturday's duelist on main
#   bash <(git show origin/duelist-loop:tools/duelist_sunday.sh) --status     # one screen
#   bash <(git show origin/duelist-loop:tools/duelist_sunday.sh) --check      # steps 1-4 only: never starts
# The approved code runs from its own worktree ($WT), never from your checkout: your checkout's auto-sync pushes
# HEAD to main, so a detached branch there would merge it unreviewed. Its duel records still go to your checkout's
# docs/duels (--records), which your auto-sync pushes as before. Never writes to the game itself.
# ---- Sunday settings: the Duel Lab's recommendation (SUNDAY v2, 00:45). Check them at 08:00; env vars override. ----
COMMIT="${COMMIT:-origin/duelist-loop}"     # the approved commit (pin the sha the re-audit approves)
SET="${SET:-C}"                             # docs/duel_sets.json: C (robust), A (SAFE) or today
POLICY="${POLICY:-code}"                    # code: code decides, Haiku writes the words; llm: the models decide
FLAGS="${FLAGS:---model claude-opus-5-5 --effort low --negotiator-model claude-haiku-4-5 --failover-s 8}"
AUTOSWITCH="${AUTOSWITCH:-0}"               # 1: also run the Duel Lab's one-way switch rule (C → A, A → today)
BY="${BY:-Aleks}"
OLD_FLAGS="${OLD_FLAGS:---negotiator-model claude-sonnet-5-5 --effort medium --negotiator-effort low}"   # Saturday's
# ------------------------------------------------------------------------------------------------------------------
set -u
MAIN="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "run it from inside your checkout of the repo"; exit 1; }
WT="${WT:-$MAIN/../team5-duelist-sunday}"
UV="$HOME/.local/bin/uv"; [ -x "$UV" ] || UV="$(command -v uv)"
say() { printf '%s %s\n' "$(date +%H:%M:%S)" "$*"; }
die() { say "ABORT: $*"; exit 1; }
procs() { pgrep -fl "agents.duelist run|duelist/supervise.sh|duel_loop.py switch" 2>/dev/null; }

status() {
  echo "=== duelist status $(date +%H:%M:%S) ==="
  for d in "$WT" "$MAIN"; do
    [ -d "$d" ] && echo "$(basename "$d"): $(git -C "$d" log --oneline -1 2>/dev/null) [$(git -C "$d" rev-parse --abbrev-ref HEAD 2>/dev/null)]"
  done
  p="$(procs)"; echo "processes:"; if [ -n "$p" ]; then echo "$p" | sed 's/^/  /'; else echo "  none"; fi
  [ -f "$WT/run/duel_params.json" ] && { echo "params ($WT/run/duel_params.json):"; sed 's/^/  /' "$WT/run/duel_params.json"; }
  log="$(ls -t "$WT"/logs/duelist/supervise-*.log "$MAIN"/logs/duelist/supervise-*.log 2>/dev/null | head -1)"
  [ -n "$log" ] && { echo "last lines of $log:"; tail -8 "$log" | sed 's/^/  /'; }
  curl -s --max-time 5 "${BAZAAR_URL:-https://bazaar.causaprima.ai}/api/clock" | python3 -c \
    'import sys,json; c=json.load(sys.stdin); print("clock: tick", c.get("tick"), "doors", c.get("doors"), "tick_s", c.get("tick_seconds"))' 2>/dev/null
}

stop_all() {
  pkill -f "duelist/supervise.sh" 2>/dev/null; pkill -f "duel_loop.py switch" 2>/dev/null; sleep 1
  pkill -f "agents.duelist run" 2>/dev/null
  for _ in 1 2 3 4 5 6 7 8 9 10; do procs >/dev/null || return 0; sleep 1; done
  die "a duelist process is still running: $(procs | tr '\n' ' ')"
}

start_in() {   # dir, records, flags...
  local dir="$1" rec="$2"; shift 2
  mkdir -p "$dir/logs/duelist"
  local log="$dir/logs/duelist/supervise-$(date +%Y%m%d-%H%M%S).log"
  (cd "$dir" && set -a && . "$MAIN/.env" && set +a && \
    nohup agents/duelist/supervise.sh "$@" --records "$rec" >"$log" 2>&1 </dev/null &)
  say "started in $dir: supervise.sh $* --records $rec (log $log)"
}

case "${1:-start}" in
  --status) status; exit 0 ;;
  --rollback)
    say "ROLLBACK: stopping every duelist on this machine"; stop_all
    git -C "$MAIN" diff --quiet HEAD -- agents engine || die "uncommitted code in $MAIN: commit or stash it by hand first"
    git -C "$MAIN" fetch -q origin && git -C "$MAIN" checkout -q main && git -C "$MAIN" pull -q --rebase origin main \
      || die "could not bring $MAIN to origin/main"
    (cd "$MAIN" && "$UV" run python -m pytest -q tests/test_duelist.py >/dev/null 2>&1) || die "duelist tests red on main"
    # main has no params file support: Saturday's constants, Saturday's flags (docs/duelist-runbook.md)
    start_in "$MAIN" "$MAIN/docs/duels" $OLD_FLAGS
    sleep 8; status; exit 0 ;;
  start|""|--check) ;;
  *) echo "usage: duelist_sunday.sh [--status | --check | --rollback]"; exit 2 ;;
esac

say "1/6 fetch and check out $COMMIT in $WT"
git -C "$MAIN" fetch -q origin || die "git fetch failed"
sha="$(git -C "$MAIN" rev-parse --verify -q "$COMMIT^{commit}")" || die "no commit $COMMIT"
if [ -d "$WT/.git" ] || [ -f "$WT/.git" ]; then
  git -C "$WT" diff --quiet HEAD || die "$WT has local changes: remove the worktree or commit them"
  git -C "$WT" checkout -q --detach "$sha" || die "checkout failed in $WT"
else
  git -C "$MAIN" worktree add -q --detach "$WT" "$sha" || die "worktree add failed"
fi
say "   $WT at $(git -C "$WT" log --oneline -1)"

say "2/6 the full test suite"
out="$(cd "$WT" && "$UV" run --project "$WT" python -m pytest -q tests 2>&1)"; code=$?
echo "$out" | tail -1
[ $code -eq 0 ] || { echo "$out" | grep -E '^(FAILED|ERROR)' | head; die "tests red: not starting"; }

say "3/6 install the approved set $SET as the whole params file"
(cd "$WT" && python3 tools/duel_loop.py use "$SET" --by "$BY") || die "set $SET refused"

say "4/6 one duelist per machine"
if procs >/dev/null; then die "a duelist is already running here: $(procs | tr '\n' ' '). Stop it, or use --rollback"; fi

if [ "${1:-}" = "--check" ]; then say "--check: steps 1-4 passed; not starting"; status; exit 0; fi

say "5/6 start: --policy $POLICY $FLAGS"
start_in "$WT" "$MAIN/docs/duels" --policy "$POLICY" $FLAGS
if [ "$AUTOSWITCH" = 1 ]; then
  (cd "$WT" && nohup python3 tools/duel_loop.py switch --records "$MAIN/docs/duels" \
    >"$WT/logs/duelist/switch-$(date +%Y%m%d-%H%M%S).log" 2>&1 </dev/null &)
  say "   the switch rule runs too (kill switch: touch $WT/run/duel_switch.off)"
fi

say "6/6 status"
sleep 10; status
