# Team 5 — The Bazaar (Causa Prima, Madrid, Oct 2–4)

Start with `STATUS.md` (live numbers, auto-updated every 5 min) and `LOG.md` (what each of us did and what came of it), then `PLAN.md` (who owns what) and `CROSSWALK.md` (what the real rules change, and how the research and the simulations fit together).

**Write only in your own file: `team/aleks.md`, `team/dani.md` or `team/lucas.md`.** Keep its **Now** line current, and after every run, experiment or decision add one line at the top of its log: `time · what · result · next`. Never edit another person's file, `STATUS.md` (written by a script) or `LOG.md` (findings and experiments, maintained by Lucas). Because nobody shares a file, pushes never conflict; logs also merge with `merge=union` (`.gitattributes`). Pull before, push right after. This is how the three of us, and each of our Claude Code sessions, stay in sync.

## Source of truth

`bazaar-kit/RULES.md` and the live server (`GET /api/schedule`, `/api/clock`, `/api/levels`) beat everything in `docs/` and `research/`. Both were written before the rules came out, assuming a single 1v1 price duel.

## Map

| Path | What | Owner |
|---|---|---|
| `bazaar-kit/` | The organisers' kit: SDK, starter agent, starter broker, `RULES.md`. Don't edit it; copy out of it | organisers |
| `docs/` | Simulations, test bench results and the leading duel agent (Clock-Standing) | Aleks |
| `research/` | Evidence base (`01`), offense (`02`), defense (`03`), red team (`04`), sponsor (`05`), hypotheses and experiment plan (`06`), spec kit (`07`), field-tested MIT prompts. `_data/` holds the MIT competition data behind `01`; the two files over 30 MB are left out | Lucas |
| `CROSSWALK.md` | Research × simulations × real rules, hypothesis by hypothesis | team |
| `STATUS.md` | Live numbers from the server. Written only by `tools/status.py`; don't edit by hand | Lucas's machine |
| `LOG.md` | Findings, experiments E1-E7, history | Lucas |
| `team/*.md` | Each person's Now line and log | each owner |
| `agents/duelist/` | The duel agent (Clock-Standing). `uv run python -m agents.duelist --help`; runbook in `docs/duelist-runbook.md` | Aleks |
| `engine/` | The LLM engine agents run on: `Model` interface, Claude provider in `claude.py` | Aleks |
| `agents/dealers/` | `abuela_bot.py`: negotiated dealer deals within the 270 P cash floor | Lucas |
| `tools/` | `daemons.sh` (start/stop/status of every long-running process), `collector.py` (all game data → `data/`), `metrics.py` (→ `intel/metrics.md`), `status.py`, `watch.py` (live events for a Monitor), `team_sync.sh`, `gitsync.py` | Lucas |
| `intel/` | `GAME.md` (rules + measured facts), `metrics.md` (live facts), `scout.md` / `judge.md` / `strategy.md` (LLM analysts, advisory), `ORCHESTRATOR.md` (runbook for the unattended operator session) | Lucas |
| `agents/analyst/` | `analyst.py --role scout|judge|strategist`: the analysts (Claude API, our credits) | Lucas |
| `agents/trader/` | `loop.py` (auto-accept), `autoflip.py` (fill teams' bids from Abuela), `trade.py` (manual), `flip.py` | Lucas |

## Rules for anyone working here, humans and Claude Code alike

- **Never commit a key.** `BAZAAR_KEY`, `BROKER_KEY` and `ANTHROPIC_API_KEY` live in `.env`, which is gitignored. Start from `.env.example`.
- **One team key, shared limits.** Every process that uses the team key shares 5 requests per second, 1 accept per tick, 1 message per conversation per tick, 6 open conversations and 30 open offers (`GET /api/clock` → `limits`).
- **One live script per job, one owner** (`PLAN.md`): duels → Aleks; dealers and our market → Lucas. A script writes only to its own job's endpoints, and announces start and stop in the team chat. Anything else stays read-only: `me`, `clock`, `schedule`, `levels`, `dealers`, `catalog`, `duels`.
- **Scripts wait for the server's tick** (`b.wait_tick()`), never a fixed sleep: the tick goes 60 s → 30 s → 15 s and can move.
- **Budget:** the $100 of API credits each is for the agent runtime and simulations. Claude Code runs on personal plans.
