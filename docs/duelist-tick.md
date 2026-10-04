# Sunday tick-decay duelist

Live `run` now defaults to tick-based decay: silence costs value every tick. It uses Opus low strategy and Sonnet low negotiation, with a 12-second whole-decision ceiling, an 8-second strategy budget and a 3-second writing budget. The server's `next_tick_in` shortens the decision budget when we start late, reserving one second to submit the move. Model deadlines do not guarantee network delivery time.

After stopping the existing duelist and passing the full suite:

```bash
agents/duelist/supervise.sh --model claude-opus-5-5 --effort low --negotiator-model claude-sonnet-5-5 --negotiator-effort low --decay-mode tick
```

Do not run this alongside another duelist. The older pinned Sunday worktree does not contain these changes.

A validated strategist band authorizes immediate acceptance this tick and the next. Code compares full price/day worth, including offers better than the band's best. Uncertain day readings, changed private limits and stale bands disable the shortcut. It also checks the newly generated band before calling the writer. A qualifying counteroffer interrupts an outstanding model call. An optional strategist estimate authorizes break-even acceptance when current surplus is at least 90% of the risk-adjusted next-tick surplus at 10% decay.

Fixed step floors/caps and deliberate opening waits are disabled in tick mode; the strategist reconsiders each tick. If the writer times out, code sends the validated target in plain words. Reservation-value checks remain mandatory.

Reusable prefixes warm automatically within two game minutes of the next session while idle. To warm manually shortly before a session, using only the model API:

```bash
uv run python -m agents.duelist warmup
```

Warm-up logs and each model-call record report cache creation/read tokens and latency. A zero-token cache report means no hit/write was verified. Warm-up failures never block live decisions. `--no-warm-cache` disables automatic warming. `--decay-mode exchange` retains the historical replay behavior.
