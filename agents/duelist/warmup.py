"""Warm only Claude's reusable prompt prefixes; no game requests or duel actions."""
from __future__ import annotations

import asyncio
from typing import Any

from engine import Model

from .agent import BandPlan, Decision, tick_prefix


async def warm_models(strategist: Model, negotiator: Model) -> list[dict[str, Any]]:
    async def warm(role: str, model: Model) -> dict[str, Any]:
        # Warm the primary, without touching the live failover circuit.
        provider = getattr(model, "primary", model)
        fn = getattr(provider, "warmup", None)
        if fn is None:
            return {"role": role, "model": model.label, "skipped": "provider has no warmup"}
        try:
            result = await asyncio.wait_for(fn(BandPlan if role == "strategist" else Decision,
                                              tick_prefix(role)), 20.0)
            return {"role": role, **result}
        except Exception as e:
            return {"role": role, "model": provider.label, "error": str(e)}

    return list(await asyncio.gather(warm("strategist", strategist), warm("negotiator", negotiator)))
