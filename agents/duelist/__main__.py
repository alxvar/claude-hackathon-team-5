"""Run from the repo root (BAZAAR_URL, BAZAAR_KEY and ANTHROPIC_API_KEY from the environment or a .env file):

    uv run python -m agents.duelist probe            # what the game shows now: clock, duel sessions, our duels (raw JSON)
    uv run python -m agents.duelist smoke            # one turn of a made-up duel through the models; sends nothing
    uv run python -m agents.duelist run --dry-run    # play live duels, but only print the moves
    uv run python -m agents.duelist run              # play live duels
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

from bazaar_sdk import Bazaar
from engine.claude import Claude, require_credentials

from .agent import DuelAgent
from .model import DuelView, Observation, Offer, Role, Turn
from .runner import DuelRunner, Log

LOGS = Path(__file__).resolve().parents[2] / "logs" / "duelist"


def bazaar(wait_on_tick: bool = False) -> Bazaar:
    return Bazaar(os.environ.get("BAZAAR_URL", "https://bazaar.causaprima.ai"), os.environ["BAZAAR_KEY"],
                  wait_on_tick=wait_on_tick)


def models(a: argparse.Namespace) -> tuple[Claude, Claude]:
    require_credentials()
    strategist = Claude(model=a.model, effort=a.effort, thinking_off=a.thinking_off)
    negotiator = Claude(model=a.negotiator_model or a.model, effort=a.negotiator_effort or a.effort,
                        thinking_off=a.thinking_off)
    return strategist, negotiator


def probe(_: argparse.Namespace) -> None:
    b = bazaar()
    out = {"clock": b.clock(), "duel_sessions": [u for u in b.schedule().get("upcoming", [])
                                                 if u.get("action") == "duels"],
           "duels": b.duels(), "duels_done": b.duels(done=True)}
    LOGS.mkdir(parents=True, exist_ok=True)
    path = LOGS / f"probe-tick{out['clock'].get('tick')}.json"
    path.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    print(f"\nsaved to {path}")


def smoke(a: argparse.Namespace) -> None:
    """One turn of a made-up duel: we sell at a cost of 40; they bid 25 then 30; we asked 70."""
    view = DuelView(duel_id="smoke", role=Role.SELLER, limit=40, item="a Malasaña rare card (MAL-11)",
                    rival="Rival-7", issues=["price", "days"] if a.days else ["price"],
                    days_weight=2 if a.days else None, decay=0.06, duel_ticks=12)
    d = (lambda p: Offer(price=p, days=4 if a.days else None))
    turns = [Turn(mine=True, text="70 P: it's a rare from a sought-after page.", offer=d(70), tick=1),
             Turn(mine=False, text="Way too much. 25.", offer=d(25), tick=1),
             Turn(mine=False, text="Fine, 30, and that's generous.", offer=d(30), tick=2)]
    obs = Observation(view=view, turns=turns, rival_offer=d(30), tick=3, ticks_left=10)
    strategist, negotiator = models(a)
    agent = DuelAgent(view, strategist, negotiator)
    move = asyncio.run(agent.respond(obs))
    print(json.dumps({"action": move.action, "price": move.price, "days": move.days, "text": move.text,
                      **move.meta}, indent=2, default=str))


def run(a: argparse.Namespace) -> None:
    strategist, negotiator = models(a)
    runner = DuelRunner(bazaar(), strategist, negotiator, dry_run=a.dry_run, log=Log(LOGS), decay=a.decay,
                        duel_ticks=a.duel_ticks, poll_s=a.poll)
    try:
        asyncio.run(runner.run())
    except KeyboardInterrupt:
        print(f"\nstopped; model spend this run about ${runner.spent_usd:.2f}; log {runner.log.path}")


def main() -> None:
    load_dotenv(find_dotenv(usecwd=True))
    p = argparse.ArgumentParser(prog="agents.duelist", description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe", help="print and save what the game shows now")
    for name, fn in (("smoke", smoke), ("run", run)):
        s = sub.add_parser(name)
        s.set_defaults(fn=fn)
        s.add_argument("--model", default="claude-opus-5-5", help="strategist model (and negotiator by default)")
        s.add_argument("--effort", default="low", choices=["low", "medium", "high", "xhigh", "max"])
        s.add_argument("--negotiator-model", help="e.g. claude-sonnet-5-5 or claude-haiku-4-5 for a faster turn")
        s.add_argument("--negotiator-effort", choices=["low", "medium", "high"])
        s.add_argument("--thinking-off", action="store_true", help="Sonnet 5.5 only: thinking between_tools")
        if name == "smoke":
            s.add_argument("--days", action="store_true", help="a two-issue duel (price and delivery day)")
        else:
            s.add_argument("--dry-run", action="store_true", help="decide and print, but send nothing")
            s.add_argument("--decay", type=float, help="override the session's decay per tick")
            s.add_argument("--duel-ticks", type=int, help="override the session's ticks per duel")
            s.add_argument("--poll", type=float, default=2.0, help="seconds between polls (two reads each)")
    sub.choices["probe"].set_defaults(fn=probe)
    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
