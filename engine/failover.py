"""A `Model` that falls back to a second model when the first one fails or is too slow.

After `trip` failures in a row the primary is skipped for `cooldown_s`, so an outage costs one slow turn, not
one per turn. Raises LLMError only when both models fail.
"""
from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field

from pydantic import BaseModel

from . import LLMError, Model, Reply


@dataclass
class Failover:
    primary: Model
    backup: Model
    timeout_s: float = 20.0          # the primary's budget before we ask the backup
    trip: int = 2
    cooldown_s: float = 120.0
    failures: int = 0
    skip_until: float = 0.0
    log: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.primary.label} (backup {self.backup.label})"

    async def parse(self, schema: type[BaseModel], system: str, messages: list[dict[str, str]]) -> Reply:
        if time.monotonic() >= self.skip_until:
            try:
                r = await asyncio.wait_for(self.primary.parse(schema, system, messages), self.timeout_s)
                self.failures = 0
                return r
            except (LLMError, TimeoutError) as e:
                self.failures += 1
                if self.failures >= self.trip:
                    self.skip_until = time.monotonic() + self.cooldown_s
                self.log.append(f"{self.primary.label}: {e!r}")
            except asyncio.CancelledError:
                # A stage deadline must cancel us, not launch work outside its budget.
                self.failures += 1
                if self.failures >= self.trip:
                    self.skip_until = time.monotonic() + self.cooldown_s
                raise
        return await self.backup.parse(schema, system, messages)
