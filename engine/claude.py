"""The Anthropic provider for `engine.Model`: Claude through the official SDK, structured output only."""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import anthropic
from pydantic import BaseModel, ValidationError

from . import LLMError, Reply

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

    async def parse(self, schema: type[BaseModel], system: str, messages: list[dict[str, str]]) -> Reply:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            # An agent's system prompt is the same every turn: cache it.
            "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
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
        pin, pout = PRICES.get(self.model, (0.0, 0.0))
        u = msg.usage
        return Reply(parsed=parsed, latency_s=latency, input_tokens=u.input_tokens, output_tokens=u.output_tokens,
                     cost_usd=(u.input_tokens * pin + u.output_tokens * pout) / 1e6, model=msg.model)
