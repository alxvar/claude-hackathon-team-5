"""Our duel agent for The Bazaar: regateo's Clock-Standing (ranged/v4/clock-standing), ported to the duel API.

A strategist call, which knows our limit, sets the price band for the turn; a negotiator call, which doesn't,
picks the price inside it and writes the message; code only holds the move to the band and the hard limits.

Changes from regateo's v4 for the duels (docs/plan-clock-standing-on-bazaar.md §4.2):
- offers are read from the structured fields, not from the text ("words persuade, structure binds");
- the clock is in ticks, and the strategist is told that a deal loses value with every tick (`decay`);
- with the `days` issue, the strategist also picks a delivery day and every priced message carries one;
- prices are whole primas, rounded toward our side so rounding can never cross the limit.

Run from bazaar-kit/:  uv run python -m duelist --help
"""
