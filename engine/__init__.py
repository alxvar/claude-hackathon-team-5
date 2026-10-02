"""The LLM engine: what an agent needs from a model, with no provider in it.

Agents depend only on `Model`, `Reply` and `LLMError`. The provider (Anthropic, in `engine.claude`) is
picked by whoever starts the agent, so agents can run on a fake model in tests or on another provider.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from pydantic import BaseModel


class LLMError(Exception):
    """Any failure of a model call. The agent falls back to a safe move on it."""


@dataclass
class Reply:
    parsed: BaseModel
    latency_s: float
    input_tokens: int
    output_tokens: int
    cost_usd: float
    model: str


class Model(Protocol):
    """One model setting that answers in a given schema. Raises LLMError on any failure."""

    @property
    def label(self) -> str:
        """A short name for the logs, e.g. "claude-opus-5-5/low"."""
        ...

    async def parse(self, schema: type[BaseModel], system: str, messages: list[dict[str, str]]) -> Reply: ...


__all__ = ["LLMError", "Model", "Reply"]
