"""What the agent is told about one duel: its private view, the conversation and the clock."""
from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class Role(StrEnum):
    BUYER = "buyer"
    SELLER = "seller"


def sign(role: Role) -> int:
    """+1 for a seller (a higher price is better), -1 for a buyer. `sign(role) * price` is our utility, so
    "is this better for us" is written once for both roles."""
    return 1 if role is Role.SELLER else -1


class Offer(BaseModel):
    price: int
    days: int | None = None


class Turn(BaseModel):
    """One message in the duel. Ours carry the decision we made (`decision`), for the negotiator's transcript."""
    mine: bool
    text: str = ""
    offer: Offer | None = None
    accept: bool = False
    tick: int | None = None
    decision: dict[str, Any] | None = None


class DuelView(BaseModel):
    """Everything we are told about one duel at the start. Only the strategist sees `limit` and `extra`."""
    duel_id: int | str
    role: Role
    limit: int                              # seller: our cost; buyer: our value
    currency: str = "P"
    item: str = ""
    context: str = ""                       # free text about the scenario, safe to show the negotiator
    rival: str = ""
    market: str | None = None               # whatever the game says about the market, as text
    issues: list[str] = Field(default_factory=lambda: ["price"])
    days_weight: Any = None                 # as the game gives it
    decay: float | None = None              # share of the deal's value lost per round of offers
    duel_ticks: int | None = None
    extra: dict[str, Any] = Field(default_factory=dict)   # unrecognised fields of the payload, for the strategist

    @property
    def has_days(self) -> bool:
        return "days" in self.issues


class Observation(BaseModel):
    view: DuelView
    turns: list[Turn] = Field(default_factory=list)
    rival_offer: Offer | None = None        # their standing offer, as the game states it
    tick: int | None = None
    ticks_left: int | None = None           # ticks left including the current one; None: unknown
    rounds: int | None = None               # the game's count of rounds so far; None: not given

    @property
    def ours(self) -> list[Turn]:
        return [t for t in self.turns if t.mine]

    @property
    def theirs(self) -> list[Turn]:
        return [t for t in self.turns if not t.mine]
