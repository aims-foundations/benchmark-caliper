"""User-priced estimates for additional adaptive screening, never invoice totals.

The request reservation uses serialized UTF-8 bytes plus a framing allowance as
an input-token estimate, and the configured maximum output tokens. This avoids
assuming a tokenizer or inventing a model price. It is conservative for ordinary
text requests, but is not a provider guarantee. Returned usage replaces the
estimate; requests without usage keep their reservation, including on resume.
"""

import json
import math

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AdaptiveSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)
    seed: int = Field(default=0, ge=0, le=2**32 - 1)
    max_cost_usd: float | None = Field(default=None, gt=0)
    input_price_per_million: float | None = Field(default=None, gt=0)
    cached_input_price_per_million: float | None = Field(default=None, ge=0)
    output_price_per_million: float | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def complete_prices(self):
        prices = (self.input_price_per_million, self.cached_input_price_per_million,
                  self.output_price_per_million)
        if any(price is not None for price in prices) and any(price is None for price in prices):
            raise ValueError("Supply all three token prices or leave all three unset.")
        if self.max_cost_usd is not None and prices[0] is None:
            raise ValueError("A cost ceiling requires the model's token prices.")
        if prices[0] is not None and prices[1] > prices[0]:
            raise ValueError("The cached input price cannot exceed the input price.")
        return self


def _usage_counts(usage: dict | None) -> tuple[int, int, int] | None:
    """Accept complete nonnegative token counts, with optional cache details."""
    if not isinstance(usage, dict):
        return None
    incoming, outgoing = usage.get("input_tokens"), usage.get("output_tokens")
    details = usage.get("input_tokens_details")
    if details is None:
        details = {}
    if not isinstance(details, dict):
        return None
    cached = details.get("cached_tokens", 0)
    if any(type(value) is not int or value < 0 for value in (incoming, outgoing, cached)) or cached > incoming:
        return None
    return incoming, outgoing, cached


def usage_cost(usage: dict | None, settings: dict) -> float | None:
    """Unknown usage/prices remain unknown, including failed responses."""
    counts = _usage_counts(usage)
    if settings["input_price_per_million"] is None or counts is None:
        return None
    incoming, outgoing, cached = counts
    value = ((incoming - cached) * settings["input_price_per_million"]
             + cached * settings["cached_input_price_per_million"]
             + outgoing * settings["output_price_per_million"]) / 1_000_000
    return value if math.isfinite(value) else None


def request_reservation(request: dict, settings: dict) -> float | None:
    if settings["input_price_per_million"] is None:
        return None
    incoming = len(json.dumps(request, ensure_ascii=False).encode("utf-8")) + 1024
    value = (incoming * settings["input_price_per_million"]
             + request["max_output_tokens"] * settings["output_price_per_million"]) / 1_000_000
    if not math.isfinite(value):
        raise ValueError("The request cost estimate is too large.")
    return value


def cost_summary(attempts: list[dict], settings: dict) -> dict:
    priced = settings["input_price_per_million"] is not None
    return {
        "scope": "adaptive_screening",
        "spent_usd": sum(attempt["cost_usd"] or 0 for attempt in attempts) if priced else None,
        "reserved_usd": sum(attempt["reserved_usd"] or 0 for attempt in attempts
                            if attempt["cost_usd"] is None) if priced else None,
        "unknown_attempts": sum(_usage_counts(attempt.get("usage")) is None for attempt in attempts),
        "pricing": "user_supplied" if priced else "not_configured",
        "reservation_method": "request_utf8_bytes_plus_1024_input_tokens_and_maximum_output_tokens",
        "limitation": "Estimated additional screening cost, not a guaranteed provider invoice limit. Initial screening is excluded.",
    }


def can_afford(reservation: float | None, attempts: list[dict], settings: dict) -> bool:
    ceiling = settings["max_cost_usd"]
    if ceiling is None:
        return True
    summary = cost_summary(attempts, settings)
    return reservation is not None and summary["spent_usd"] + summary["reserved_usd"] + reservation <= ceiling
