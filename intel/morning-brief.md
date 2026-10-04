# Morning brief, Sunday (Chief, 07:30): what each of us does. Everything else runs by itself.

The plan is `intel/sunday-final.md`. The Operator runs the game; the Chief (Lucas's "Team 5 Chief of staff" tab) decides. If something looks wrong, tell the Chief; don't touch the game by hand.

## Lucas
1. **07:30** Check the VS Code tabs for any session waiting on a permission prompt and approve it. The `zsh` tab with `caffeinate` stays open.
2. **08:30** WhatsApp → **Team 9**: the combined text at the top of `intel/market-sunday.md` §0.5 ("¡Hola Team 9! Dos cosas…"). Then → **Team 15** (MAL-07, the last MAL card): «¡Hola Team 15! ¿Nos vendés tu MAL-07 repetida? Cuando te avisemos, te dejamos una oferta de compra a ~30 P en v26 (mercado de Team 2, 0 %), dirigida a Team 15: solo tenés que aceptarla. ¡Gracias!»
3. **08:30** WhatsApp → one club member (Team 7 or 9) for the CHA last card: «¡Hola! Hoy vamos a necesitar una carta de Chamberí (CHA). Si te sale alguna repetida, ¿nos avisás? Te la compramos en el mercado del club que prefieras. ¡Gracias!»
4. **09:00** Ask the organisers' desk, in person: *"If one venue beats the stall's efficiency and nobody else does, does it get the full Market Test points for that session?"* Tell the Chief the answer.
5. Share the club page (https://claude.ai/artifact/9HVLftiHAKMwgPwTQbLff1, Share menu) with the members only when you want to; the 08:30 deals don't depend on it.

## Dani
1. **08:30** WhatsApp → **Team 7**: the combined text at the top of `intel/market-sunday.md` §0.5 ("¡Hola Team 7! Dos cosas…").
2. **≈ 08:35** After the Chief confirms Team 16 is not a rival: the Team 16 rows (RET-01 to Team 2, RET-03 to Team 4, then to Team 16) from §0.5, in order.
3. When a listing appears, send the "ya está publicada… ¡aceptala!" nudge from §0.5.
4. Review the Operator's log (`team/lucas.md` top) if you want; any "stop" or "undo" goes to the Chief.
5. After 15:00: pitch.

## Aleks (duelist; final sha re-audited: GO)
1. **Before 10:30**, in your checkout, in zsh (keep the braces):
   `SHA=29aa1bed66962959ce633492d84bbc321385c7e7`
   `COMMIT=$SHA bash <(git show "${SHA}:tools/duelist_sunday.sh") --check` (expect "steps 1-4 passed"), then
   `COMMIT=$SHA AUTOSWITCH=1 bash <(git show "${SHA}:tools/duelist_sunday.sh")`
2. It runs in its own worktree (no merge), refuses if a duelist already runs, installs set C (code policy, Haiku text, failover 8 s), and switches C → A once if the deal rate drops.
3. Status: `--status`. Stop: `--stop`. Back to Saturday's duelist: `--rollback`.
4. Don't pipe its output (`| tee` etc. hangs it). Don't re-run start/`--check` while it's live.
5. Your PLAN.md #32 has the same; details in `docs/duelist-loop.md` and `intel/duelist-reaudit.md`.
