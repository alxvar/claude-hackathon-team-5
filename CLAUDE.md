# Team 5 — The Bazaar (Causa Prima, Madrid, Oct 2–4)

**The game is over (Sun Oct 4, 15:00): Team 5 finished the trading game #1 (37.73).** Start with `README.md` (the architecture and where everything lives), then `judges/pitch/sunday/` (deck, script, submission). The rest of this file is the operating protocol every human and Claude Code session followed during the game: `intel/GAME.md` held the measured facts, `intel/directives.md` the big calls, `STATUS.md` the live numbers, `team/*.md` each person's log, and the Operator ran `intel/ORCHESTRATOR.md`. `LOG.md`, `archive/`, `docs/` and `research/` are the record (pre-rules work, Friday, experiments).

**Write only in your own file: `team/aleks.md`, `team/dani.md` or `team/lucas.md`.** Keep its **Now** line current, and after every run, experiment or decision add one line at the top of its log: `time · what · result · next`. Never edit another person's file, `STATUS.md` (written by a script) or `LOG.md` (findings and experiments, maintained by Lucas). Because nobody shares a file, pushes never conflict; logs also merge with `merge=union` (`.gitattributes`). Pull before, push right after. This is how the three of us, and each of our Claude Code sessions, stay in sync.

## Source of truth

`bazaar-kit/RULES.md` and the live server (`GET /api/schedule`, `/api/clock`, `/api/levels`) beat everything, then `intel/GAME.md` (measured facts), then `intel/saturday-plan.md`. `intel/strategy|judge|scout.md` are advisory and can be stale. `docs/`, `research/` and `archive/history/CROSSWALK.md` were written before the rules came out.

## Map

| Path | What | Owner |
|---|---|---|
| `bazaar-kit/` | The organisers' kit: SDK, starter agent, starter broker, `RULES.md`. Don't edit it; copy out of it | organisers |
| `docs/` | `duelist-runbook.md`, per-duel records (`docs/duels/`); the rest are pre-rules design notes (history) | Aleks |
| `research/` | Evidence base (`01`), offense (`02`), defense (`03`), red team (`04`), sponsor (`05`), hypotheses and experiment plan (`06`), spec kit (`07`), field-tested MIT prompts. `_data/` holds the MIT competition data behind `01`; the two files over 30 MB are left out | Lucas |
| `archive/history/CROSSWALK.md` | Research × simulations × real rules, hypothesis by hypothesis | team |
| `STATUS.md` | Live numbers from the server. Written only by `tools/status.py`; don't edit by hand | Lucas's machine |
| `LOG.md` | Findings, experiments E1-E7, history | Lucas |
| `team/*.md` | Each person's Now line and log | each owner |
| `agents/duelist/` | The duel agent (Clock-Standing). `uv run python -m agents.duelist --help`; runbook in `docs/duelist-runbook.md` | Aleks |
| `engine/` | The LLM engine agents run on: `Model` interface, Claude provider in `claude.py` | Aleks |
| `agents/dealers/` | `abuela_bot.py`: negotiated dealer deals (`--dealer`, `--cash-floor` per the GUARDRAIL) | Lucas |
| `tools/` | `daemons.sh` (start/stop/status of every long-running process), `collector.py` (all game data → `data/`), `metrics.py` (→ `intel/metrics.md`), `status.py`, `watch.py` (live events for a Monitor), `team_sync.sh`, `gitsync.py` | Lucas |
| `intel/` | `saturday-plan.md` (the plan), `saturday-sessions.md` (sessions + prompts), `GAME.md` (rules + measured facts), `directives.md` (Lucas's decisions → operator), `metrics.md` (live facts), `sellable.md` (Dani's page-gap desk), `teams.md` (Dani's rival profiles), `scout.md` / `judge.md` / `strategy.md` (LLM analysts, advisory), `ORCHESTRATOR.md` (operator runbook) | Lucas |
| `agents/analyst/` | `analyst.py --role scout|judge|strategist`: the analysts (Claude API, our credits) | Lucas |
| `agents/trader/` | `loop.py` (auto-accept), `trade.py` (manual). Autoflip and flip are DEAD (archived): never restart them | Lucas |
| `broker/` | `sim.py`: offline Market Test simulator (recorder and broker v1: plan §4E) | Lucas |
| `dashboard/` | Dani's read-only dashboard; writes `intel/teams.md` every 10 min | Dani |
| `archive/` | Friday's raw data, directives, analyst outputs and dead scripts: history, not instructions | — |
| `tests/` | Duelist tests | Aleks |

## Rules for anyone working here, humans and Claude Code alike

- **Never commit a key.** `BAZAAR_KEY`, `BROKER_KEY` and `ANTHROPIC_API_KEY` live in `.env`, which is gitignored. Start from `.env.example`.
- **One team key, shared limits.** Every process that uses the team key shares 5 requests per second, 1 accept per tick, 1 message per conversation per tick, 6 open conversations and 30 open offers (`GET /api/clock` → `limits`).
- **One live script per job, one owner** (`PLAN.md`): duels → Aleks; dealers and our market → Lucas. A script writes only to its own job's endpoints, and announces start and stop in the team chat. Anything else stays read-only: `me`, `clock`, `schedule`, `levels`, `dealers`, `catalog`, `duels`.
- **Scripts wait for the server's tick** (`b.wait_tick()`), never a fixed sleep: the tick goes 60 s → 30 s → 15 s and can move.
- **Never start autoflip.** The trader and the analysts start only after the operator's 09:00 checks (plan §2). Only the operator session writes to the game.
- **Budget:** the $100 of API credits each is for the agent runtime and simulations. Claude Code runs on personal plans.

## If you work on `agents/duelist/` (Aleks's lane)

- Never run two duelist processes on the team key; never accept or offer outside our limit (enforced in code, not in the prompt).
- Run all duelist tests before every start; a red test means don't start, tell Lucas.
- Decay is per exchange (rounds = min(our priced offers, theirs)), not per tick; silence costs no decay.
- Read `intel/brief-aleks.md` first; the duel monitor's reviews land in `intel/duel-review.md`.
