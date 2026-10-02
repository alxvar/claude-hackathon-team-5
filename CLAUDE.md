# Team 5 — The Bazaar (Causa Prima, Madrid, Oct 2–4)

Start with `CROSSWALK.md`: what the real rules change, and how the research and the simulations fit together.

## Source of truth

`bazaar-kit/RULES.md` and the live server (`GET /api/schedule`, `/api/clock`, `/api/levels`) beat everything in `docs/` and `research/`. Both were written before the rules came out, assuming a single 1v1 price duel.

## Map

| Path | What | Owner |
|---|---|---|
| `bazaar-kit/` | The organisers' kit: SDK, starter agent, starter broker, `RULES.md`. Don't edit it; copy out of it | organisers |
| `docs/` | Simulations, test bench results and the leading duel agent (Clock-Standing) | Aleks |
| `research/` | Evidence base (`01`), offense (`02`), defense (`03`), red team (`04`), sponsor (`05`), hypotheses and experiment plan (`06`), spec kit (`07`), field-tested MIT prompts. `_data/` holds the MIT competition data behind `01`; the two files over 30 MB are left out | Lucas |
| `CROSSWALK.md` | Research × simulations × real rules, hypothesis by hypothesis | team |

## Rules for anyone working here, humans and Claude Code alike

- **Never commit a key.** `BAZAAR_KEY`, `BROKER_KEY` and `ANTHROPIC_API_KEY` live in `.env`, which is gitignored. Start from `.env.example`.
- **One team key, shared limits.** Every process that uses the team key shares 5 requests per second, 1 accept per tick, 1 message per conversation per tick, 6 open conversations and 30 open offers (`GET /api/clock` → `limits`). Only the runtime we agree on acts on the live server. Everything else stays read-only: `me`, `clock`, `schedule`, `levels`, `dealers`, `catalog`, `duels`.
- **Don't run `starter_agent.py` against the live server without telling the team.** It spends team cash on a pack.
- **Budget:** the $100 of API credits each is for the agent runtime and simulations. Claude Code runs on personal plans.
