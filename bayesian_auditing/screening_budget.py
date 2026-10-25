"""User-priced estimates for additional adaptive screening, never invoice totals.

The request reservation uses serialized UTF-8 bytes plus a framing allowance as
an input-token estimate, and the configured maximum output tokens. The input
reservation includes the configured screening model's default cache-write rate.
Long-context multipliers apply when the input estimate crosses the model's tier.
It is conservative for ordinary text requests, but is not a provider guarantee.
Returned usage replaces the estimate; requests without usable usage keep their
reservation, including on resume.
"""

import json
import math

from pydantic import BaseModel, ConfigDict, Field, model_validator


# These are total write rates, not surcharges. Base dollar prices remain supplied
# by the user. Keep this policy separate from the adaptive sampling version so
# correcting billing never changes seeded queue decisions.
# https://developers.openai.com/api/docs/guides/prompt-caching
# https://developers.openai.com/api/docs/models/gpt-6-luna
COST_POLICY = {
    "version": 2,
    "model": "gpt-6-luna",
    "cache_write_30m_input_multiplier": 1.25,
    "cache_write_12h_input_multiplier": 2.5,
    "reservation_cache_lifetime": "30m",
    "missing_write_breakdown": "unknown_usage_keep_reservation",
    "supplied_prices": "short_context_rates_for_account_processing_tier_and_region",
    "long_context_above_input_tokens": 272_000,
    "long_context_input_multiplier": 2.0,
    "long_context_output_multiplier": 1.5,
}


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


def _usage_counts(usage: dict | None) -> tuple[int, int, int, int, int] | None:
    """Validate disjoint ordinary input, reads, and both write lifetimes.

    Older usage without write fields means zero writes (SDK serialization may
    fill these absent fields with null). Positive writes without a complete
    lifetime breakdown cannot be priced reliably and remain unknown.
    """
    if not isinstance(usage, dict):
        return None
    incoming, outgoing = usage.get("input_tokens"), usage.get("output_tokens")
    details = usage.get("input_tokens_details")
    if details is None:
        details = {}
    if not isinstance(details, dict):
        return None
    cached = details.get("cached_tokens", 0)
    written = details.get("cache_write_tokens")
    if written is None:
        written = 0
    if (any(type(value) is not int or value < 0 for value in (incoming, outgoing, cached, written))
            or cached + written > incoming):
        return None
    try:
        if not math.isfinite(incoming + outgoing):
            return None
    except OverflowError:
        return None
    breakdown = details.get("cache_write_tokens_details")
    if breakdown is None:
        if written:
            return None
        short_write, long_write = 0, 0
    elif isinstance(breakdown, dict):
        short_write, long_write = breakdown.get("ttl_30m_tokens"), breakdown.get("ttl_12h_tokens")
        if (any(type(value) is not int or value < 0 for value in (short_write, long_write))
                or short_write + long_write != written):
            return None
    else:
        return None
    return incoming - cached - written, outgoing, cached, short_write, long_write


def _context_multipliers(incoming: int) -> tuple[float, float]:
    if incoming > COST_POLICY["long_context_above_input_tokens"]:
        return COST_POLICY["long_context_input_multiplier"], COST_POLICY["long_context_output_multiplier"]
    return 1.0, 1.0


def usage_cost(usage: dict | None, settings: dict) -> float | None:
    """Unknown usage/prices remain unknown, including failed responses."""
    counts = _usage_counts(usage)
    if settings["input_price_per_million"] is None or counts is None:
        return None
    ordinary, outgoing, cached, short_write, long_write = counts
    input_multiplier, output_multiplier = _context_multipliers(ordinary + cached + short_write + long_write)
    input_cost = ((ordinary
                   + short_write * COST_POLICY["cache_write_30m_input_multiplier"]
                   + long_write * COST_POLICY["cache_write_12h_input_multiplier"])
                  * settings["input_price_per_million"]
                  + cached * settings["cached_input_price_per_million"])
    value = (input_cost * input_multiplier
             + outgoing * settings["output_price_per_million"] * output_multiplier) / 1_000_000
    return value if math.isfinite(value) else None


def request_reservation(request: dict, settings: dict) -> float | None:
    if settings["input_price_per_million"] is None:
        return None
    if request.get("model") != COST_POLICY["model"]:
        raise ValueError("Cost reservations require the configured GPT-6 Luna pricing policy.")
    # The pipeline uses default caching. Reject a changed request policy instead
    # of under-reserving 12-hour writes or assuming another model's cache rates.
    if "prompt_cache_options" in request or "prompt_cache_retention" in request:
        raise ValueError("Cost reservations require the default 30-minute cache policy.")
    incoming = len(json.dumps(request, ensure_ascii=False).encode("utf-8")) + 1024
    input_multiplier, output_multiplier = _context_multipliers(incoming)
    value = (incoming * settings["input_price_per_million"]
             * COST_POLICY["cache_write_30m_input_multiplier"] * input_multiplier
             + request["max_output_tokens"] * settings["output_price_per_million"] * output_multiplier) / 1_000_000
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
        "policy": dict(COST_POLICY),
        "reservation_method": "request_utf8_bytes_plus_1024_at_30m_cache_write_rate_and_maximum_output_tokens_with_context_tier",
        "limitation": "Estimated additional screening cost, not a guaranteed provider invoice limit. Initial screening is excluded.",
    }


def can_afford(reservation: float | None, attempts: list[dict], settings: dict) -> bool:
    ceiling = settings["max_cost_usd"]
    if ceiling is None:
        return True
    summary = cost_summary(attempts, settings)
    return reservation is not None and summary["spent_usd"] + summary["reserved_usd"] + reservation <= ceiling
