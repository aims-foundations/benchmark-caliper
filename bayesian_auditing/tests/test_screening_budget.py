"""Additional-screening cost estimates and conservative unknown-use accounting."""

from copy import deepcopy
from itertools import product
import math

import pytest
from pydantic import ValidationError

from bayesian_auditing.screening_budget import (
    AdaptiveSettings, can_afford, cost_summary, request_reservation, usage_cost,
)


def settings(**overrides):
    return AdaptiveSettings(input_price_per_million=2.0, cached_input_price_per_million=0.5,
                            output_price_per_million=8.0, **overrides).model_dump()


def usage(incoming=1000, outgoing=250, cached=400):
    return {"input_tokens": incoming, "output_tokens": outgoing,
            "input_tokens_details": {"cached_tokens": cached}}


def attempt(*, tokens=None, cost=None, reserved=0.02, status="complete"):
    return {"usage": tokens, "cost_usd": cost, "reserved_usd": reserved, "status": status}


def test_default_settings_allow_unpriced_runs_and_retain_explicit_scope():
    config = AdaptiveSettings().model_dump()
    assert config["seed"] == 0
    assert config["max_cost_usd"] is None
    assert usage_cost(usage(), config) is None
    assert request_reservation({"max_output_tokens": 250}, config) is None
    assert can_afford(None, [], config)
    summary = cost_summary([], config)
    assert summary["spent_usd"] is None and summary["reserved_usd"] is None
    assert summary["pricing"] == "not_configured"
    assert summary["scope"] == "adaptive_screening"
    assert "Initial screening is excluded" in summary["limitation"]
    assert "not a guaranteed provider invoice limit" in summary["limitation"]


@pytest.mark.parametrize("present", list(product((False, True), repeat=3)))
def test_token_rates_are_all_present_or_all_absent(present):
    keys = ["input_price_per_million", "cached_input_price_per_million", "output_price_per_million"]
    fields = {key: value for key, value, included in zip(keys, (2.0, 0.5, 8.0), present) if included}
    if all(present) or not any(present):
        AdaptiveSettings(**fields)
    else:
        with pytest.raises(ValidationError, match="all three"):
            AdaptiveSettings(**fields)


@pytest.mark.parametrize("name", ["max_cost_usd", "input_price_per_million",
                                 "cached_input_price_per_million", "output_price_per_million"])
@pytest.mark.parametrize("value", [float("inf"), float("-inf"), float("nan")])
def test_cost_settings_must_be_finite(name, value):
    config = settings()
    config[name] = value
    with pytest.raises(ValidationError):
        AdaptiveSettings.model_validate(config)


@pytest.mark.parametrize("name", ["max_cost_usd", "input_price_per_million", "output_price_per_million"])
@pytest.mark.parametrize("value", [0.0, -0.1, True, "1"])
def test_positive_money_settings_are_strict(name, value):
    config = settings()
    config[name] = value
    with pytest.raises(ValidationError):
        AdaptiveSettings.model_validate(config)


def test_cached_rate_may_be_zero_but_not_negative_or_above_uncached_rate():
    config = settings()
    config["cached_input_price_per_million"] = 0.0
    assert AdaptiveSettings.model_validate(config).cached_input_price_per_million == 0
    for value in (-0.1, 2.1):
        config["cached_input_price_per_million"] = value
        with pytest.raises(ValidationError):
            AdaptiveSettings.model_validate(config)


def test_cost_ceiling_requires_rates_and_unrecognized_settings_are_rejected():
    with pytest.raises(ValidationError, match="token prices"):
        AdaptiveSettings(max_cost_usd=1.0)
    with pytest.raises(ValidationError):
        AdaptiveSettings(max_items=160)
    assert AdaptiveSettings.model_validate(settings(max_cost_usd=1.0)).max_cost_usd == 1


@pytest.mark.parametrize("seed", [-1, 2**32, True, "1", 1.5])
def test_seed_range_is_strict(seed):
    with pytest.raises(ValidationError):
        AdaptiveSettings(seed=seed)


def test_cached_input_is_charged_once_at_its_own_rate():
    config = settings()
    # 600 uncached at $2/M + 400 cached at $0.5/M + 250 output at $8/M.
    assert usage_cost(usage(), config) == pytest.approx(0.0034)
    assert usage_cost(usage(cached=1000), config) == pytest.approx(0.0025)
    assert usage_cost(usage(incoming=0, outgoing=0, cached=0), config) == 0
    assert usage_cost({"input_tokens": 1000, "output_tokens": 250}, config) == pytest.approx(0.004)


@pytest.mark.parametrize("tokens", [
    None, {}, "unknown", {"input_tokens": 1}, {"output_tokens": 1},
    usage(incoming=-1), usage(outgoing=-1), usage(cached=-1), usage(cached=1001),
    usage(incoming=1.5), usage(outgoing="250"), usage(cached=True),
    usage(incoming=True), usage(outgoing=False),
    {"input_tokens": 1000, "output_tokens": 250, "input_tokens_details": "unknown"},
    {"input_tokens": 1000, "output_tokens": 250, "input_tokens_details": [1]},
])
def test_missing_or_invalid_usage_keeps_cost_unknown(tokens):
    assert usage_cost(tokens, settings()) is None


def test_request_reservation_counts_unicode_bytes_and_maximum_output_without_cache_discount():
    config = settings()
    request = {"input": "a", "max_output_tokens": 250}
    original = deepcopy(request)
    base = request_reservation(request, config)
    assert base > 1024 * 2 / 1_000_000 + 250 * 8 / 1_000_000
    assert request == original
    # UTF-8 é occupies two bytes, while a occupies one.
    unicode_request = {**request, "input": "é"}
    assert request_reservation(unicode_request, config) - base == pytest.approx(2 / 1_000_000)
    more_output = {**request, "max_output_tokens": 251}
    assert request_reservation(more_output, config) - base == pytest.approx(8 / 1_000_000)
    config["cached_input_price_per_million"] = 0
    assert request_reservation(request, config) == base


def test_unrepresentable_request_reservation_is_rejected():
    config = settings()
    config["input_price_per_million"] = 1e308
    with pytest.raises(ValueError, match="too large"):
        request_reservation({"input": "Question", "max_output_tokens": 250}, config)


def test_known_usage_replaces_reservation_and_unknown_attempts_keep_it_on_resume():
    config = settings(max_cost_usd=0.1)
    history = [attempt(tokens=usage(), cost=0.0034, reserved=0.02),
               attempt(status="unknown", reserved=0.03),
               attempt(tokens=usage(0, 0, 0), cost=0.0, reserved=0.04)]
    original = deepcopy(history)
    summary = cost_summary(history, config)
    assert summary["spent_usd"] == pytest.approx(0.0034)
    assert summary["reserved_usd"] == pytest.approx(0.03)
    assert summary["unknown_attempts"] == 1
    assert summary == cost_summary(deepcopy(history), deepcopy(config))
    assert history == original
    assert can_afford(0.06, history, config)
    assert not can_afford(0.07, history, config)
    assert not can_afford(None, history, config)


def test_failed_requests_with_returned_usage_still_cost_money():
    config = settings(max_cost_usd=0.005)
    history = [attempt(tokens=usage(), cost=0.0034, reserved=0.02, status="error")]
    assert cost_summary(history, config)["spent_usd"] == pytest.approx(0.0034)
    assert cost_summary(history, config)["reserved_usd"] == 0
    assert not can_afford(0.002, history, config)


@pytest.mark.parametrize("tokens", [None, {}, {"input_tokens": 1000}, usage(cached=1001),
                                   {"input_tokens": 1000, "output_tokens": "unknown"}])
def test_unknown_attempt_count_tracks_unusable_usage_even_if_object_is_nonempty(tokens):
    config = settings()
    history = [attempt(tokens=tokens, cost=None, reserved=0.03)]
    summary = cost_summary(history, config)
    assert summary["unknown_attempts"] == 1
    assert summary["spent_usd"] == 0
    assert summary["reserved_usd"] == 0.03


def test_known_usage_without_prices_is_not_unknown_usage():
    config = AdaptiveSettings().model_dump()
    history = [attempt(tokens=usage(), cost=None, reserved=None)]
    summary = cost_summary(history, config)
    assert summary["unknown_attempts"] == 0
    assert summary["spent_usd"] is None and summary["reserved_usd"] is None


def test_ceiling_allows_exact_fit_and_rejects_an_extra_request():
    config = settings(max_cost_usd=1.0)
    history = [attempt(tokens=usage(), cost=0.5, reserved=0.75),
               attempt(reserved=0.25, status="unknown")]
    assert can_afford(0.25, history, config)
    assert not can_afford(math.nextafter(0.25, math.inf) + 1e-12, history, config)
    assert can_afford(1e20, history, settings())  # Pricing alone is not a ceiling.
