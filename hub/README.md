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
