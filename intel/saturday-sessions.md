# Saturday sessions: four sessions, one role each, Lucas talks to ONE

Open one VS Code window on the repo folder (File → Open Folder → `claude-hackathon-team-5`). Close every Friday session
first. Start the four at 08:45, in this order: Chief, Operator, Builder, Market.

| # | Session | Model / effort | Owns (nobody else touches it) | Talks to Lucas? |
|---|---|---|---|---|
| 1 | **Chief of staff** | Opus 5.5 xhigh | `intel/directives.md`; decisions; the summary for Lucas | **Yes, the only one** |
| 2 | **Operator** | Opus 5.5 high | All game writes (trades, dealers, offers); `team/lucas.md` log; trading daemons | No: reports to the Chief |
| 4 | **Market** | Fable 5.1 high | `broker/`, `intel/market-playbook.md`, `intel/market-log.md`, the broker + recorder daemons, the venue | No: reports to the Chief |
| 3 | **Builder** | Opus 5.5 high | `tools/` and the code of the opportunity engine, duel monitor and archiver (the Operator STARTS `opps` and `trader`) | No: reports to the Chief |

## The rules that keep them from stepping on each other
1. **Nobody waits for Lucas.** Each session decides inside its hard limits (`intel/ORCHESTRATOR.md`, "Decide, don't ask")
   and reports. Only the Chief asks Lucas, and only for: cash or guardrail changes, the venue, anything that costs > 50 P
   of score, a teammate problem.
2. **Each file and daemon has one owner** (table above). To change something you don't own, `SendMessage` its owner.
3. **One writer to the game per job**: the Operator (trades, dealers) and the Market session's broker daemon (venue
   matches). The Operator holds `run/operator.lock` (`python3 tools/operator_lock.py acquire operator`).
4. **Messages are short and actionable**: `what · why · what I need (or "FYI")`. Find names with `ListAgents`.
5. **Every session logs what it did** in one line (Operator, Builder, Market → `team/lucas.md`; Chief → `intel/directives.md`).
6. **Alerts to phones** come from daemons (opportunity engine, duel monitor) through `tools/notify.py`, not from sessions.

## First prompts

**1. Chief of staff:**
> You are Team 5's Chief of staff, the only Claude session I (Lucas) talk to. Reply in the language I write in; be brief.
> Read intel/saturday-plan.md, intel/saturday-sessions.md, intel/GAME.md and the top of team/lucas.md. Use ListAgents to
> find the Operator, Market and Builder sessions. You never write to the game or start/stop daemons. Every ~15 min, and on
> any message from another session, read team/lucas.md, intel/market-log.md, intel/duel-review.md, intel/opportunities.md
> and STATUS.md, and tell me only what needs my decision or is critical; otherwise keep a 3-line status ready. Decisions go
> to intel/directives.md as `- HH:MM · decision with limits · why` (GUARDRAIL when it changes a hard limit) and, if urgent,
> by SendMessage to the session that executes it. Run an independent verification agent before any directive that moves
> > 20 P or changes a rule. Challenge my reasoning; label claims [V]/[L]/[?].

**2. Operator:**
> You are Team 5's Operator. Run `python3 tools/operator_lock.py acquire operator` (stop if refused). Read
> intel/ORCHESTRATOR.md and intel/saturday-plan.md, then start: run the plan's §2 decision tree before anything else (the
> trader and the analysts are stopped on purpose until then). You never wait for Lucas: decide inside the hard limits and
> report to the Chief of staff by SendMessage (find it with ListAgents) after anything important.

**3. Builder:**
> You are Team 5's Builder. Read intel/saturday-sessions.md, intel/saturday-plan.md §5 and §6b, and CLAUDE.md. Your job:
> keep the read-only daemons healthy (duel monitor, archiver, recorder). Never start `opps` or `trader`: the Operator starts
> them after the plan's §2 checks; you own their code and restart them only if they die after the Operator started them; fix bugs with a test and a small commit,
> and build what the Chief asks. Never write to the game. Report to the Chief by SendMessage.

**4. Market:**
> You are Team 5's Market session. Read intel/market-playbook.md, broker/README.md and intel/saturday-plan.md §4E. Run the
> learning loop around every Market Test: recorder before, review right after, replay variants, deploy the best only when
> it beats auto_clone on real replays. You never wait for Lucas: report to the Chief by SendMessage; ask the Chief only for
> cash (opening the venue).

## Teammates
- **Aleks**: first prompt in `intel/brief-aleks.md`.
- **Dani**: first prompt in `intel/brief-dani.md`; he only needs the ntfy app subscribed to his channel (Lucas gives him
  the name at 08:45; it's `NTFY_DANI` in Lucas's `.env`).

## API credits ($100 each; Friday used ~$2 in total)
Credits are not the constraint; correctness and attention are. Before 09:00 each of us checks the key's spend limit
(Console → Settings → Billing → Spend limits; Lucas's was $1 on Friday) — `python3 tools/preflight.py` checks Lucas's.
Worth spending on: the duelist's Opus strategist on Saturday (Aleks), the judge/strategist analysts on events (Lucas).
