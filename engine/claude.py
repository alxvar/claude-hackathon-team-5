"""The Anthropic provider for `engine.Model`: Claude through the official SDK, structured output only."""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import anthropic
from pydantic import BaseModel, ValidationError

from . import CACHE_PREFIX_END, LLMError, Reply

# USD per MTok (input, output), for the running cost line in the logs.
PRICES = {"claude-opus-5-5": (4.0, 20.0), "claude-sonnet-5-5": (2.0, 10.0), "claude-haiku-4-5": (1.0, 5.0)}


def require_credentials() -> None:
    """Without a key every call fails and the agent only plays its fallback. Fail before playing."""
    profile = Path(os.environ.get("ANTHROPIC_CONFIG_DIR", Path.home() / ".config" / "anthropic"))
    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN") or profile.exists()):
        raise SystemExit("No Claude credentials: set ANTHROPIC_API_KEY in the repo's .env (see .env.example).")


@dataclass
class Claude:
    """One model setting. `effort` controls thinking depth: on Opus 5.5 thinking can't be turned off, so `low`
    keeps a turn fast; on Sonnet 5.5, `thinking_off` sends `between_tools`, its lowest setting."""
    model: str = "claude-opus-5-5"
    effort: str = "low"
    thinking_off: bool = False
    max_tokens: int = 8000
    timeout_s: float = 60.0
    fallbacks: bool = True          # server-side refusal fallback ("default" routing)
    _client: Any = field(default=None, repr=False)

    def __post_init__(self) -> None:
        self._client = anthropic.AsyncAnthropic(timeout=self.timeout_s, max_retries=1)

    @property
    def label(self) -> str:
        return f"{self.model}/{self.effort}"

    def _request(self, system: str, messages: list[dict[str, str]]) -> tuple[Any, dict[str, Any]]:
        prefix, boundary, context = system.partition(CACHE_PREFIX_END)
        blocks = [{"type": "text", "text": prefix, "cache_control": {"type": "ephemeral"}}]
        if boundary and context:
            # A second breakpoint also reuses this duel's private context on later turns.
            blocks.append({"type": "text", "text": context, "cache_control": {"type": "ephemeral"}})
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": blocks,
            "messages": messages,
        }
        haiku = self.model.startswith("claude-haiku")
        if not haiku:                           # Haiku 4.5 rejects effort, and has no server-side fallback
            kwargs["output_config"] = {"effort": self.effort}
        if self.thinking_off and self.model == "claude-sonnet-5-5":
            kwargs["thinking"] = {"type": "between_tools"}
        api = self._client.messages
        if self.fallbacks and not haiku:
            kwargs["betas"] = ["server-side-fallback-2026-07-01"]
            kwargs["fallbacks"] = "default"
            api = self._client.beta.messages
        return api, kwargs

    def _usage(self, msg: Any, latency: float, parsed: BaseModel | None = None) -> Reply:
        pin, pout = PRICES.get(self.model, (0.0, 0.0))
        u = msg.usage
        created = getattr(u, "cache_creation_input_tokens", 0) or 0
        read = getattr(u, "cache_read_input_tokens", 0) or 0
        read_rate = 0.05 if self.model == "claude-opus-5-5" else 0.1
        cost = ((u.input_tokens + 1.25 * created + read_rate * read) * pin + u.output_tokens * pout) / 1e6
        return Reply(parsed=parsed, latency_s=latency, input_tokens=u.input_tokens, output_tokens=u.output_tokens,
                     cost_usd=cost, model=msg.model, cache_creation_input_tokens=created,
                     cache_read_input_tokens=read)

    async def warmup(self, schema: type[BaseModel], prefix: str) -> dict[str, Any]:
        """Write the exact model/effort/schema prefix, without parsing the deliberately truncated reply."""
        api, kwargs = self._request(prefix, [{"role": "user", "content": "Prepare for the next duel."}])
        kwargs["max_tokens"] = 1
        config = kwargs.setdefault("output_config", {})
        config["format"] = {"type": "json_schema", "schema": anthropic.transform_schema(schema)}
        start = time.perf_counter()
        try:
            msg = await api.create(**kwargs)
        except (anthropic.APIError, TypeError) as e:
            raise LLMError(f"cache warmup: {e}") from e
        r = self._usage(msg, time.perf_counter() - start)
        return {"model": r.model, "latency_s": round(r.latency_s, 2), "cost_usd": round(r.cost_usd, 6),
                "cache_creation_input_tokens": r.cache_creation_input_tokens,
                "cache_read_input_tokens": r.cache_read_input_tokens,
                "cached": bool(r.cache_creation_input_tokens or r.cache_read_input_tokens)}

    async def parse(self, schema: type[BaseModel], system: str, messages: list[dict[str, str]]) -> Reply:
        api, kwargs = self._request(system, messages)
        start = time.perf_counter()
        try:
            msg = await api.parse(output_format=schema, **kwargs)
        except ValidationError as e:
            raise LLMError(f"response does not match {schema.__name__}: {e}") from e
        except anthropic.APIStatusError as e:
            raise LLMError(f"{e.status_code}: {e.message}") from e
        except (anthropic.APITimeoutError, anthropic.APIConnectionError) as e:
            raise LLMError(f"{type(e).__name__}: {e}") from e
        except TypeError as e:                  # e.g. no credentials: the SDK raises before sending
            raise LLMError(f"{type(e).__name__}: {e}") from e
        latency = time.perf_counter() - start
        if msg.stop_reason == "refusal":
            raise LLMError(f"{msg.model} refused")
        parsed = getattr(msg, "parsed_output", None)
        if parsed is None:
            raise LLMError(f"no parsed output (stop_reason={msg.stop_reason})")
        return self._usage(msg, latency, parsed)
