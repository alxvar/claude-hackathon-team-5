# Live dashboard (read-only)

What every team is doing, in one page: score over time, each team's inferred strategy (what it collects, what it
sells off, whether it trades with teams or dealers), the El Rastro board with the real team behind each "anonymous"
offer, opportunities and rival bids at our private values, who last bought the cards we want, prices by rarity,
dealer haggling per team, duels and the schedule.

    python dashboard/server.py        # open http://127.0.0.1:8765

On Windows, double-click `dashboard/start.bat`: it starts the server in the background (it keeps running after
VS Code or the window closes) and opens the browser. Every teammate can run their own copy with their own key.

- **Never writes to the game.** Public routes are read without the team key; only `me` and `duels` use it.
- **Light on the shared limits:** about 5-8 requests per tick, 0.4 s apart.
- **The key stays local:** it comes from `BAZAAR_KEY`, `.env` or `~/bazaar_key.txt`, and the page is served on
  127.0.0.1 only. `--no-key` shows public data only.
- **History** is cached in `logs/dashboard/` (gitignored). The feed only keeps the last ~20 ticks, so the
  dashboard knows what happened while it was running; leave it on.
- **The team hub (optional):** with `HUB_READER_URL` in `.env` (ask Aleks; see `hub/README.md`) and `psycopg`
  installed, it also reads the hub at start and every 5 rounds, read-only, and merges the events, leaderboard
  snapshots and `/api/me` rows it missed (Friday's early settlements, anything while it was off). The header shows
  `hub synced HH:MM:SS`. `--no-hub` turns it off; without the URL it runs as before.
- Strategy labels and "who holds" are inferences from the feed: starting cards and pack pulls are invisible.

Owner: Dani.
