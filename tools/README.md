# tools/ · daemons, guards and helpers (all started by `daemons.sh`)

`daemons.sh start|stop|status [name…]` runs every long-lived process (19 defined; each restarts itself).

| Job | Files |
|---|---|
| **Sense** (read-only) | `collector.py` / `collectors.py` (feed, me, leaderboard → `data/`), `metrics.py` (→ `intel/metrics.md`), `status.py` (→ `STATUS.md` every 5 min), `watch.py` (live events to the Operator), `reactor.py` (public event stream → BUY / DENY lines + phone alerts), `news.py` (organisers' news), `hints.py` + `eggs.py` (easter eggs in dealer replies), `album.py` (what public data proves about each team's album), `known.py` (holdings teams told us) |
| **Find deals** | `opportunities.py` (page gaps → phone alerts), `bargains.py`, `matchmaker.py` (club matchmaker: spares × missing cards across teams), `v10_radar.py` (best buyer for each ask on our venue) |
| **Guards** | `policy.py` (who we may trade with), `arbiter.py` (the team's one accept per tick), `operator_lock.py`, `preflight.py` (keys and spend limits before start) |
| **Duels** | `duel_monitor.py` (reviews every wave → `intel/duel-review.md`), `duel_sim_v2.py` (the Duel Lab simulator), `duel_gates.py` (the Duel Lab's switch rule, advisory) |
| **Humans in the loop** | `notify.py` (ntfy phone alerts to Lucas and Dani), `alerts.py` (the alert policy every sender goes through) |
| **Team sync** | `gitsync.py`, `team_sync.sh` (pull at every prompt, push after every turn), `archive_round.py` |
| `sunday/` | One-off Sunday scripts: sequenced page closers (`mal_close.py`, `cha11_*.py`), venue ads, duel windows |
