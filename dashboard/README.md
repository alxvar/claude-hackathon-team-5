# Live dashboard (read-only)

What every team is doing, in one page: score over time, each team's inferred strategy (what it collects, what it
sells off, whether it trades with teams or dealers), the El Rastro board with the real team behind each "anonymous"
offer, opportunities and rival bids at our private values, who last bought the cards we want, prices by rarity,
dealer haggling per team, duels and the schedule.

    python dashboard/server.py        # open http://127.0.0.1:8765

**Two views.** `/` is the compact live view (`live.html`): six KPI tiles; the leaderboard as the organisers show it (score /60 split into negotiating and market, level, badges, album, rarest card, the countdown to the next standings) plus each team's move since the previous snapshot and its gap to us (click a team: its race and why it jumped); our market (every open offer on our stall v10 with the real team behind it, offers addressed to one team included, and the trades settled on it; the public board shows only offers open to anyone, so the rest comes from the feed); the race with a projection to the close (each team's trend over the last 90 game minutes, fading over about an hour, ± its typical volatility: an 80 % range; statistical only); every battle we fight (duels and dealer
haggles, live ones first) with its price chart (us vs them vs our limit, or the card's worth to us) and messages,
click one for the full chat; our deck set by set; the race around us; and our record per arena (duels, dealers,
El Rastro, Market Test). `?f=duel|dealer` filters the battles; `#d6191` or `#t2351` opens one. `/full` is the
detailed view below (`index.html`), with every tab.

**The race explorer** (⤢ Explore on the race card, or `#race`, `#race:t10`, `#race:t10:5`): every team's score on a
wall-clock axis (day and hour; nights and pauses take no room), range buttons (last 2 h, each day, all), drag to zoom,
shift + drag to pan, double-click to reset; pick the teams to draw; click a line or a team to list its jumps of 1 point
or more, each with why: the part that moved (negotiating or market), the field's drift (the median change of the teams
with no deal then: the board is relative), its own deals and the trades on its stall, a page completed, and what ran
then (duels, a Market Test, a dealer opening); click a jump to zoom on it. Wall times come from the history of
`STATUS.md` (`tools/status.py` writes its local time, tick and game hour every few minutes): local git only.

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

**The judges' showcase:** http://127.0.0.1:8765/show (brief: `judges/dashboard-brief.md`; design: Figma
"Team 5 · Judges showcase", https://www.figma.com/design/picVx0KcLHR9uY0ctMuVTu). One page, eight sections, live from
`/api/data` plus the story texts in `judges/show.json`, which it re-reads every minute (edit it, no restart). It adds no
request to the game; "last seen" in the diagram is the last commit of each file on GitHub. No external files, so it works
offline; light or dark follows the system (button top right, or `?theme=light|dark`); stacks on a phone.

Owner: Dani.
