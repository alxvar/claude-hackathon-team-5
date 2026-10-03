# Brief: the judges' showcase dashboard (design in Figma, then build)

> For: the Claude Code session that designs this in Figma and then builds it, and for Dani/Lucas reviewing it.
> Written Sat 13:27. Judging format and criteria are still unknown (desk Q7); RULES.md only says "Judges 40: your
> ideas and your craft". Numbers below are examples from 13:27: on the page every figure is live or sourced.

## 1. Goal

One screen, projected or on a laptop, that a judge understands in under a minute: **who we are, how the system
works, what it achieved today, and what we learned by measuring**. It is the visual companion to `judges/demo.md`
(6 slides) and reuses its content. It is not the team's ops dashboard (that stays as it is).

Craft signals the judges should see: live data (not screenshots), every number with its source and a [V]/[L] label,
humans set limits while agents act, mistakes turned into rules.

## 2. Format

- Figma: one page "Showcase", frames **1440×900** (laptop / projector) and **390×844** (phone, the same sections stacked).
- Build: a new route `/show` on the existing dashboard server (`dashboard/server.py`, `dashboard/show.html`), fed by
  `/api/data` plus a small static file `judges/show.json` (story texts Dani edits). **Read-only, no extra request to the
  game** (the duelist shares the team's 5 requests/s).
- Light and dark, reusing the dashboard's color tokens (`dashboard/index.html` `:root`); our team in `--series-1` blue,
  everyone else neutral grey.

## 3. Sections (top to bottom)

| # | Section | Content | Data (live unless marked) |
|---|---|---|---|
| 1 | **Hero** | "Team 5 · three humans, many agents". Big: rank and score now; small: Negotiating / Market split, cash, pages complete | `me.score` (rank 5, 28.15, neg 20.65, market 7.5), `me.cash` 184 |
| 2 | **The race** | Score of all 18 teams over the day, ours highlighted, the top 4 labelled; markers on our big moves | `lb_hist`, `moves` |
| 3 | **Why we moved** | Waterfall of our score change across Duels I: duels, ladder, the 40 % re-weighting; each bar with its cause in one line | `me_hist`; split from `intel/score-model.md` [L]; log Sat 12:57 in `team/dani.md` |
| 4 | **Duels** | Duels I: 30 deals of 34 (88 %) vs field 76 %; 478.9 P of 591 P surplus, 19 % lost to rounds; "0-1 rounds kept 95 %, 7+ rounds kept 57 %"; one duel transcript as a chat card | `duelmon`, `duelview`; `team/aleks.md` 13:20-13:22 (static) |
| 5 | **How it works** | The architecture diagram from demo.md slide 2 (facts → advice → decisions → actions), node type marked code / agent / human, each node with "last seen" | static diagram; last-seen from git log of `intel/*.md` (optional) |
| 6 | **Learning loop** | 4 cards "measured mistake → rule → code": MAL-07 −11.8 → never above value; SAL-06 fed t17 → feeding rule; v10 trade −5.2 market → collector-buys only; duel 181 +10.6 left → accept in-limit by 2 ticks | `judges/show.json` (static, sources in `DECISIONS.md`) |
| 7 | **What we measured** | 6 facts as chips with [V]/[L]: per-trade cap 50, dealer gains don't score, duel result formula, Saturday Negotiating = 0.6 × trades + duels, page bonus, game hour = wall hour | `judges/demo.md` "What we measured" (static) |
| 8 | **Cost** | Model spend: duelist $1.62 for 34 scored duels; analysts; Claude Code on personal plans | `judges/demo.md` "Cost ledger" (static, fill TBDs) |

## 4. Components to design

Stat tile (big number, label, delta, source line) · race line chart (many grey lines, one blue) · waterfall bar ·
label chip [V] / [L] / [?] · learning-loop card (three steps with arrows) · architecture node (code / agent / human
variants) · chat bubble (us / rival) · "live" indicator with last update time.

## 5. Rules for the design

- Every number has a visible source (small grey line) and, if it is a finding, its [V]/[L] label.
- Never show a price we might use in the room, our cash floor or anything from `.env`.
- No team is shamed: rivals appear only as lines in the race and in aggregate numbers.
- Big type, few words: each section has one headline sentence (the "message" lines of demo.md).

## 6. Order of work for the next session

1. Read this file and `judges/demo.md`.
2. Figma: tokens → components (section 4) → the 1440 frame → the phone frame. Share the link with the team.
3. Dani reviews; then build `/show` in `dashboard/` (Dani's folder), test it against the running server, restart it.
4. Log each step in `team/dani.md`.
