#!/usr/bin/env bash
# Team sync for Claude Code, wired in .claude/settings.json. Runs on the machine of whoever uses Claude Code here.
#   pull: on session start and on every prompt, pulls main and tells Claude what teammates pushed since last time
#         (their commits and files, and LOG.md's "Now" board when it changed). Prints nothing if nothing changed.
#   push: when Claude finishes a turn, commits whatever changed (manual edits included; .env and logs/ are
#         gitignored) and pushes it, so the others see your work within minutes.
# Never blocks Claude: every failure is reported on stderr and the script exits 0.
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/..}" || exit 0
mode="$1"
state=".git/team_sync_seen"
me="$(git config user.name)"

if [ "$mode" = "pull" ]; then
  git pull --rebase --autostash -q origin main >/dev/null 2>&1 || echo "team_sync: git pull failed, resolve by hand" >&2
  head="$(git rev-parse HEAD)"
  seen="$(cat "$state" 2>/dev/null)"
  [ "$head" = "$seen" ] && exit 0
  echo "$head" > "$state"
  range="${seen:+$seen..}HEAD"
  [ -z "$seen" ] && range="HEAD~10..HEAD"
  hashes="$(git log --no-merges --format='%H %an' "$range" -- . ':(exclude)STATUS.md' 2>/dev/null \
            | grep -v -- " $me\$" | cut -d' ' -f1 | head -15)"
  [ -z "$hashes" ] && exit 0
  echo "TEAM SYNC (auto, from GitHub): teammates pushed since your last prompt:"
  for h in $hashes; do git log -1 --format='- %h %an, %ar: %s' "$h"; done
  echo "Files they touched:"
  for h in $hashes; do git show --name-only --format= "$h" -- . ':(exclude)STATUS.md'; done | sort -u | sed 's/^/  /' | head -20
  for f in team/*.md; do
    git diff --quiet "${seen:-HEAD~10}" HEAD -- "$f" 2>/dev/null && continue
    echo "$f changed:"; grep -m1 '^\*\*Now:\*\*' "$f"; grep '^- ' "$f" | head -3
  done
  for f in CLAUDE.md PLAN.md; do  # instructions: inject the changed lines, so they apply even mid-session
    git diff --quiet "${seen:-HEAD~10}" HEAD -- "$f" 2>/dev/null && continue
    echo "$f CHANGED. These lines are now the team's instructions (+ added, - removed); follow them:"
    git diff -U0 "${seen:-HEAD~10}" HEAD -- "$f" | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)' | head -40
  done
  git diff --quiet "${seen:-HEAD~10}" HEAD -- LOG.md 2>/dev/null || echo "LOG.md (findings/experiments) changed: read it."
  echo "Write only in your own team/<name>.md; never edit someone else's file (CLAUDE.md)."
  exit 0
fi

if [ "$mode" = "push" ]; then
  git add -A >/dev/null 2>&1
  if ! git diff --cached --quiet; then
    files="$(git diff --cached --name-only | head -6 | tr '\n' ' ')"
    git commit -q -m "auto ($me): $files" >/dev/null 2>&1
  fi
  git pull --rebase --autostash -q origin main >/dev/null 2>&1 || { git rebase --abort >/dev/null 2>&1; echo "team_sync: pull conflict, push by hand" >&2; exit 0; }
  git push -q origin HEAD:main >/dev/null 2>&1 || echo "team_sync: push failed" >&2
  git rev-parse HEAD > "$state" 2>/dev/null
  exit 0
fi
