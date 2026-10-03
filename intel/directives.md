# Directives (Lucas's strategy session → operator, analysts, teammates)

_Written by the strategy session. It never touches the game: no trades, no bots. The operator decides and executes inside its hard limits (ORCHESTRATOR.md, "Decide, don't ask"); Lucas changes a limit only with a line containing GUARDRAIL. Format: `- HH:MM · decision with limits · why`. Newest block on top. Labels: **[Verified]** measured on our own deals or read from the server; **[Likely]** fitted or inferred; **[Open]** unknown._

## Sat 02:20 — market venue and cash floor (Lucas delegated both decisions to the operator, who decided on the data)

- 03:30 · GUARDRAIL · Until the Market session's venue decision (right after the first Market Test) the cash floor is 370 P (100 + the 270 P bond); after it, 100 (or 100 above the bond if the venue is open) · keeps the venue option open; final review Sat 03:20.
- 02:20 · GUARDRAIL · Cash floor 100 P on Saturday (was 200); 0 by Sunday 14:00 (everything into non-negative buys, CHA first). Venue bond, if paid, comes before the floor. Pass it to bots: trader `--cash-floor 100`, dealer bot `--cash-floor 100`, opportunity engine `CASH_FLOOR=100` · cash scores nothing at the end; the RET page needs ~280 P.
- 02:20 · Market venue, staged: (1) first Market Test on the free stall with the recorder running; (2) right after it: if the stall does NOT expose `bench_offers` to us → open a `board` venue at fee 0 at once with `auto_clone` (the only way to learn), then iterate; if it does → learn on the stall and open as soon as real replays show our broker beats `auto_clone`, or a rival board venue beats the stall teams; (3) whatever happens, our venue is open, tested and supervised before Sunday 10:00 · a venue that matches like the stall earns the same half; the edge comes only from data and a better broker; Sunday's two benches weigh ~4× each.

## Sat 01:20 — repo cleanup

- 01:20 · intel/saturday-plan.md is the plan for Saturday; Friday's directives are archived in archive/fri/directives-fri.md (history, not orders) · repo cleanup, Lucas's instruction
