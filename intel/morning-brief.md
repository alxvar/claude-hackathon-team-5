# Morning brief, Sunday (Chief, 07:30): what each of us does. Everything else runs by itself.

The plan is `intel/sunday-final.md`. The Operator runs the game; the Chief (Lucas's "Team 5 Chief of staff" tab) decides. If something looks wrong, tell the Chief; don't touch the game by hand.

## Lucas
1. **07:30** Check the VS Code tabs for any session waiting on a permission prompt and approve it. The `zsh` tab with `caffeinate` stays open.
2. **08:30** WhatsApp → **Team 9**: ONLY the RET-09 text from `intel/market-sunday.md` §0.5 row 1 (not bundled with SAL-02: a two-way bundle between the same pair looks like a round trip; SAL-02 goes later, on its own). Then → **Team 15** (MAL-07, the last MAL card): «¡Hola Team 15! ¿Nos vendés tu MAL-07 repetida? Cuando te avisemos, te dejamos una oferta de compra a ~30 P en v26 (mercado de Team 2, 0 %), dirigida a Team 15: solo tenés que aceptarla. ¡Gracias!»
3. **08:30** WhatsApp → one club member (Team 7 or 9) for the CHA last card: «¡Hola! Hoy vamos a necesitar una carta de Chamberí (CHA). Si te sale alguna repetida, ¿nos avisás? Te la compramos en el mercado del club que prefieras. ¡Gracias!»
4. **08:45** At the organisers' desk, in person, two questions; tell the Chief the answers. (a) *"Our free stall v10 will host card deals we match between other teams: each one agreed by both teams, positive for both at their own values, addressed, 0% fee, no payments of any kind. Is that fine, including when the same few teams trade several times on it during the day?"* (b) *"If one venue beats the stall's efficiency and nobody else does, does it get the full Market Test points for that session?"*
5. Share the club page (https://claude.ai/artifact/9HVLftiHAKMwgPwTQbLff1, Share menu) with the members only when you want to; the 08:30 deals don't depend on it.

## Dani
1. **08:30** WhatsApp → **Team 7**: ONLY the RET-09 text from `intel/market-sunday.md` §0.5 row 1 (SAL-02 later, separately).
2. **≈ 08:35** After the Chief confirms Team 16 is not a rival: the Team 16 rows (RET-01 to Team 2, RET-03 to Team 4, then to Team 16) from §0.5, in order.
3. When a listing appears, send the "ya está publicada… ¡aceptala!" nudge from §0.5.
4. Review the Operator's log (`team/lucas.md` top) if you want; any "stop" or "undo" goes to the Chief.
5. After 15:00: pitch.

## Aleks (duelist; final sha re-audited twice: GO) = PLAN.md #32
1. **08:30**, in zsh (keep the braces): `SHA=29aa1bed66962959ce633492d84bbc321385c7e7`, then
   `bash <(git show "${SHA}:tools/duelist_sunday.sh") --status`. If Saturday's duelist is up: `COMMIT=$SHA bash <(git show "${SHA}:tools/duelist_sunday.sh") --stop`.
   Then `COMMIT=$SHA bash <(git show "${SHA}:tools/duelist_sunday.sh") --check` (expect "steps 1-4 passed").
2. **Start at R+5 min** (R = round 3's first tick, ≈ 09:05 if the clock jumps): `COMMIT=$SHA AUTOSWITCH=1 bash <(git show "${SHA}:tools/duelist_sunday.sh")`.
   It runs set C (code policy, Haiku text, failover 8 s) in its own worktree, with no merge, and switches C → A once if the deal rate drops.
3. Duels III = R + 2 game h (≈ 11:00), the Final ≈ 14:00: re-read /api/schedule and check again at 13:30.
4. Never pipe its output (it hangs); never re-run start/--check while it's live. Stop: `--stop`. Back to Saturday's duelist: `--rollback`.
5. After two waves: `tools/duel_gates.py --session 4 --params <worktree>/run/duel_params.json`. Expected: a deal rate of 0.88-0.93 with rivals that spoke, and 2-3 rounds per deal.
