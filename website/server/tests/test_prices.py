"""Tests for model price routing."""

from __future__ import annotations

from website.server.prices import cost_usd


def test_haiku_cheaper_than_sonnet() -> None:
    assert cost_usd("claude-haiku-4-5", 1000, 1000) < cost_usd(
        "claude-sonnet-4-6", 1000, 1000
    )


def test_sonnet_cheaper_than_opus() -> None:
    assert cost_usd("claude-sonnet-4-6", 1000, 1000) < cost_usd(
        "claude-opus-4-7", 1000, 1000
    )


def test_unknown_model_returns_zero() -> None:
    assert cost_usd("not-a-model", 1000, 1000) == 0.0


def test_zero_tokens_zero_cost() -> None:
    assert cost_usd("claude-opus-4-7", 0, 0) == 0.0


def test_routing_is_case_insensitive() -> None:
    assert cost_usd("CLAUDE-HAIKU-4-5", 1000, 1000) == cost_usd(
        "claude-haiku-4-5", 1000, 1000
    )
