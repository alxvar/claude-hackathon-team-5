"""Analysts: LLMs that read the facts and advise. They never trade; the orchestrator decides.

- scout (Claude Sonnet 5.5, every 5 min): what is working for the teams climbing the board, which concrete
  opportunities are open right now, what threatens us. Writes intel/scout.md.
- judge (Claude Opus 5.5, every 15 min): grades OUR strategies against their measured results (keep / kill / scale),
  checks the scout's claims against the metrics, and proposes the 3 changes with the highest expected gain.
  Writes intel/judge.md.

Both read intel/GAME.md (stable rules and measured facts) and intel/metrics.md (live facts, tools/metrics.py).

    uv run python agents/analyst/analyst.py --role scout --every 300
    uv run python agents/analyst/analyst.py --role judge --every 900
"""
import argparse
import os
import sys
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
INTEL = ROOT / "intel"
sys.path.insert(0, str(ROOT / "tools"))
import gitsync  # noqa: E402

ROLES = {
    "strategist": {"model": "claude-opus-5-5", "effort": "high", "out": "strategy.md", "brief": """You are the STRATEGIST for Team 5.
Your job is to CRACK THE GAME, not to react to it or copy other teams. Copying the leaders at best ties them; we want to
finish first every day. Reason from the rules (RULES.md is included), the measured facts, the live metrics and the
schedule. Write markdown, at most 70 lines:
## How the points really work
Model the scoring: which components exist, which are relative to the field, which are capped, and where the field is
weak right now (components where every team is near zero are the cheapest points). Use numbers from the data.
## Our winning strategy
What Team 5 should dominate, given OUR multipliers, holdings and cash, and why it beats what the leaders are doing:
a set or page (Lavapiés page, Chamberí on Sunday at 1.6x), a role (market maker, LAT/MAL/SAL supplier to collectors),
a component (Market Test, duels, ladder levels), or a combination. Be decisive and say what we stop doing.
## Levers nobody is using yet
Each with the evidence that nobody uses it and how we exploit it first.
## Plan, anchored to the schedule
Ordered moves for the rest of today and for tomorrow, each with when (schedule event or time), who (executor bot,
operator, Lucas, Dani, Aleks), and expected impact.
## Hypotheses to test
Each: the hypothesis, the cheapest experiment, the metric that decides it."""},
    "scout": {"model": "claude-sonnet-5-5", "effort": "medium", "out": "scout.md", "brief": """You are the SCOUT for Team 5.
Find what is working for the teams climbing the leaderboard and the concrete opportunities open RIGHT NOW.
Write markdown, at most 35 lines:
## Top 3 actions now
For each: the exact action (card, price, offer id or counterparty team, which executor or human does it), the evidence
from the metrics (quote the numbers), the expected effect on our neg_points or ladder, and confidence (high/med/low).
## What the climbing teams are doing
Two to four bullets, each tied to trades in the metrics.
## Threats
Up to three bullets (a team racing us for a card, a price moving against us, a leader we are feeding)."""},
    "judge": {"model": "claude-opus-5-5", "effort": "high", "out": "judge.md", "brief": """You are the JUDGE for Team 5.
You are independent from the people and bots executing. Your job: are our actions working, and what should change.
Write markdown, at most 40 lines:
## Verdict
One line: are we gaining on the leaders, holding, or falling behind, with the numbers.
## Our strategies: keep / kill / scale
One line each for every strategy you can see in our actions (dealer bot, trading loop, our bids and listings,
in-room trades): verdict and the evidence (neg_points movement, fills, time unfilled).
## Check the scout
Which of the scout's claims hold against the metrics, and which do not.
## The 3 changes with the highest expected gain
Concrete and executable, ranked; expected effect and the main risk for each."""},
}

RULES = """Ground rules for every answer:
- Use only facts present in GAME.md, the Saturday plan, Lucas's directives, the metrics, the scout's notes or our logs. If a number is not there, say "not in the data" instead of estimating it.
- Every recommendation must be executable with the tools in GAME.md ("what we can do") or by a human in the room.
- Never recommend trades that hand a leading team more value than we gain.
- Be terse; no preamble."""


def read(name, limit=12000):
    p = INTEL / name
    return p.read_text()[-limit:] if p.exists() else f"({name}: not available yet)"


def head(name, limit=6000):
    """Newest-on-top files (directives.md): the newest part is the head."""
    p = INTEL / name
    return p.read_text()[:limit] if p.exists() else f"({name}: not available yet)"


def top(path, n=30):
    """Newest-on-top logs (team/*.md): the Now line and the latest entries are the first lines."""
    p = ROOT / path
    return "\n".join(p.read_text().splitlines()[:n]) if p.exists() else "(none)"


def tail(path, n=30):
    p = ROOT / path
    return "\n".join(p.read_text().splitlines()[-n:]) if p.exists() else "(none)"


def live_game():
    sys.path.insert(0, str(ROOT / "bazaar-kit"))
    from bazaar_sdk import Bazaar
    import json
    try:
        b = Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"])
        c, sch = b.clock(), b.schedule()
        up = [f"game hour {e['at_hours']}: {e['action']} - {e.get('note', '')} {json.dumps(e.get('params', {}))[:120]}"
              for e in sch.get("upcoming", [])[:20]]
        return (f"now: game hour {c['t_hours']:.2f}, tick {c['tick']}, {c['tick_seconds']} s/tick, closes {c.get('closes')}\n"
                + "\n".join(up) + f"\nlevels: {json.dumps(b.levels())[:600]}\ndealers: "
                + json.dumps([(d['id'], d.get('status'), d.get('level'), d.get('teaser') or d.get('title')) for d in b.dealers().get('personas', [])]))
    except Exception as e:
        return f"(live game data unavailable: {e!r})"


def findings():
    t = (ROOT / "LOG.md").read_text()
    a = t.find("## Findings so far")
    return t[a:t.find("## Log", a)] if a >= 0 else "(none)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--role", choices=ROLES, required=True)
    ap.add_argument("--every", type=int, default=0, help="seconds between runs; 0 = once")
    args = ap.parse_args()
    load_dotenv(ROOT / ".env")
    role = ROLES[args.role]
    client = anthropic.Anthropic()
    while True:
        system = [{"type": "text", "text": read("GAME.md", 40000) + "\n\n" + RULES + "\n\n" + role["brief"],  # re-read: GAME.md changes
                   "cache_control": {"type": "ephemeral"}}]
        facts = (f"# Lucas's directives (decided; never recommend against them)\n{head('directives.md', 6000)}\n\n# Saturday plan\n{head('saturday-plan.md', 30000)}\n\n"
                 f"# Live metrics\n{read('metrics.md')}\n\n# Rival profiles (Dani, intel/teams.md)\n{read('teams.md', 6000)}"
                 f"\n\n# Lucas's lane: now and recent log\n{top('team/lucas.md', 16)}")
        if args.role == "strategist":
            facts += (f"\n\n# RULES.md (full)\n{(ROOT / 'bazaar-kit/RULES.md').read_text()}"
                      f"\n\n# Schedule, levels and dealers (live)\n{live_game()}"
                      f"\n\n# Findings so far (LOG.md)\n{findings()}"
                      f"\n\n# The judge's latest\n{read('judge.md', 5000)}\n\n# The scout's latest\n{read('scout.md', 4000)}")
        if args.role == "judge":
            facts += (f"\n\n# The scout's latest notes\n{read('scout.md', 5000)}"
                      f"\n\n# Our trading-loop actions (last 25)\n{tail('logs/trader.jsonl', 25)}"
                      f"\n\n# Our dealer/flip actions (last 25)\n{tail('logs/dealers/' + max((p.name for p in (ROOT / 'logs/dealers').glob('*.jsonl')), default='none'), 25)}")
        try:
            with client.messages.stream(  # streamed: 32k output exceeds the SDK's non-streaming limit
                model=role["model"], max_tokens=32000, system=system,
                output_config={"effort": role["effort"]},
                messages=[{"role": "user", "content": facts}],
            ) as stream:
                resp = stream.get_final_message()
            if resp.stop_reason == "refusal":
                text = "_The model declined this run; next run in a few minutes._"
            else:
                text = "".join(b.text for b in resp.content if b.type == "text").strip()
            if not text:  # all output went to thinking (max_tokens): keep the previous file
                print(time.strftime("%H:%M:%S"), args.role, "empty output, kept the previous file", resp.stop_reason,
                      resp.usage.output_tokens, flush=True)
                if not args.every:
                    break
                time.sleep(args.every)
                continue
            out = INTEL / role["out"]
            out.write_text(f"# {args.role.capitalize()} ({role['model']}, {time.strftime('%a %H:%M')})\n\n{text}\n")
            gitsync.push([f"intel/{role['out']}", "intel/metrics.md"], f"intel: {args.role} {time.strftime('%H:%M')}")
            print(time.strftime("%H:%M:%S"), args.role, "ok", resp.usage.input_tokens, resp.usage.output_tokens, flush=True)
        except anthropic.APIError as e:
            print(time.strftime("%H:%M:%S"), args.role, "API error:", repr(e)[:200], flush=True)
        if not args.every:
            break
        time.sleep(args.every)


if __name__ == "__main__":
    main()
