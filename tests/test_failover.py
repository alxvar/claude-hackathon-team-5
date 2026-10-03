"""engine/failover.py at 15 s ticks (audit S3): the primary's budget sits below the runner's per-decision budget, and
the runner's own cancellation counts as a failure, so the backup engages and the trip fires."""
import asyncio

import pytest

from engine import Reply
from engine.failover import Failover


class Slow:
    def __init__(self, delay, label="slow"):
        self.delay, self.label, self.calls = delay, label, 0

    async def parse(self, schema, system, messages):
        self.calls += 1
        await asyncio.sleep(self.delay)
        return Reply(None, self.delay, 1, 1, 0.0, self.label)


def test_the_default_budget_is_below_the_runners_10_s():
    assert Failover(Slow(0), Slow(0)).timeout_s <= 8.0


def test_a_slow_primary_hands_over_to_the_backup_within_the_budget():
    f = Failover(Slow(1.0, "opus"), Slow(0.0, "haiku"), timeout_s=0.05)
    r = asyncio.run(f.parse(None, "", []))
    assert r.model == "haiku" and f.failures == 1


def test_the_runners_cancellation_counts_as_a_failure_and_trips_the_primary():
    f = Failover(Slow(5.0, "opus"), Slow(0.0, "haiku"), timeout_s=10.0, trip=2)

    async def decide():                                  # the runner: wait_for(respond, budget)
        await asyncio.wait_for(f.parse(None, "", []), 0.05)

    for _ in range(2):
        with pytest.raises(asyncio.TimeoutError):
            asyncio.run(decide())
    assert f.failures == 2 and f.skip_until > 0          # tripped: the next turn goes straight to the backup
    r = asyncio.run(f.parse(None, "", []))
    assert r.model == "haiku" and f.primary.calls == 2
