# hub/: one shared copy of the game (Neon Postgres) and the demand model

Owner: Aleks. Lucas's `tools/collector.py` and Dani's dashboard keep working unchanged; they can switch to reading
the hub whenever they want.

Why: the public feed returns only the newest 500 events and has no paging (~15 ticks on Friday, a few minutes on
Sunday). Whatever no collector saw in time is lost, and until now each of our three collectors (Lucas's `data/`,
Dani's `logs/dashboard/`, the duelist's `docs/duels/feed.jsonl`) held its own partial history.

## Setup (once per machine)

1. `.env` needs `HUB_WRITER_URL` (collectors, importer, model) and/or `HUB_READER_URL` (read-only: dashboards,
   analysts, Claude sessions). Aleks shares them privately. Never commit them.
2. `uv sync` (adds `psycopg`).

## Run

| What | Command | Where |
|---|---|---|
| Collector (keyless, never uses the team key) | `nohup hub/supervise.sh collect --host <name> >/dev/null 2>&1 &` | Aleks's Mac + Lucas's machine |
| One pass (smoke test) | `uv run python -m hub.collect --once --host <name>` | anywhere |
| Load history files | `uv run python -m hub.import_files data/feed.jsonl data/leaderboard.jsonl data/me.jsonl` | whoever has them |
| Demand model | `nohup hub/supervise.sh demand >/dev/null 2>&1 &` (every 2 min) or `uv run python -m hub.demand --once` | one machine |
| Stop | `pkill -f 'hub/supervise.sh collect'; pkill -f hub.collect` | |

Two collectors write the same rows once (the server's event id is the key), so either alone keeps the record
whole. Each also appends every event to `data/hub/feed-<host>.jsonl`; if the hub was unreachable, load that file
with `hub.import_files` afterwards. Logs: `logs/hub-collect.log`, `logs/hub-demand.log`.

## Health

```sql
select * from hub.v_health;          -- one row per collector: age of its last pass, newest event id, errors
select * from hub.gaps order by at desc;   -- a full feed window whose oldest event was newer than ours
```

## Tables

| Table / view | What |
|---|---|
| `hub.events` | Every public feed event (raw `payload` jsonb), keyed by the server's id |
| `hub.offers` | Every offer seen on any venue, with its life: listed, last seen, cancelled or gone (filled/expired) |
| `hub.leaderboard`, `hub.team_snapshots` | Each leaderboard refresh; per team: score, `album_filled`, `pages_complete`, luck, level, venue |
| `hub.state`, `hub.state_history` | clock, schedule, levels, dealers, venues, catalog (latest + every distinct version) |
| `hub.cards` | The card list (set, rarity, book, print run, minted) |
| `hub.me_snapshots` | Our own `/api/me` history, imported from Lucas's and Dani's files |
| `hub.v_settlements`, `hub.v_trade_items`, `hub.v_team_trades`, `hub.v_fill_prices` | Trades, flattened |
| `hub.team_mult`, `hub.team_card_value`, `hub.opportunities`, `hub.evidence`, `hub.model_runs` | Demand model outputs |

Schema changes: edit `hub/schema.sql`, then `uv run python -m hub.setup --schema` (owner URL, Aleks).

## Demand model (`hub/demand.py`, no LLM)

For every team and card: what one more copy is worth to that team, the chance it lacks the card, and the chance the
card completes one of its pages.

- **Multipliers:** every team's six multipliers are ours in another order, so the model keeps an exact posterior over
  the 720 orders. Evidence: trades (a buyer's cost bounds its value from below, a seller's price from above; fees
  counted for the taker), the best standing bid / ask per card, bids to dealers, and net buying / dumping per set.
  Teams aren't fully rational, so every observation has a noise floor (`PARAMS`).
- **Holdings:** the last known holder of every card that was traded or listed. Starting hands and most pack pulls are
  invisible, so "lacks" is a probability (signal from a bid or a dealer request, fading with a 2-hour half-life, else a
  prior from `album_filled`).
- **Opportunities:** `sell` (our copy, the price that maximises (price − our loss) × P(the buyer's value ≥ price +
  fee), capped near the dealer's price unless the card closes their page), `buy` (a known holder, the bid that
  maximises min(cap 50, our value − price) × P(their loss ≤ price − fee)), `match` (two other teams that should swap,
  for our venue). `feeding` flags page closers to teams within 10 points of us and the top 4.
- **What it can and can't tell:** buys only bound values from below, so low multipliers show up through sells and
  dumping. On synthetic rational teams it sorts sets into the high and low groups reliably and ranks the true order
  in the top ~2 % of 720; separating 1.6 from 1.3 needs more trades. **Self-test:** every run scores the posterior
  for our own true order from our public behaviour only (`hub.model_runs.summary->'selftest'`).

```sql
select team, set, top, round(p_top::numeric, 2), n_obs from hub.team_mult order by team, e_mult desc;
select * from hub.opportunities order by exp_gain desc limit 20;
```
