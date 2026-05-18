"""Tests for the email notifier.

In v0 (no RESEND_API_KEY set) we hard-rely on the dry-run fallback so
local Docker stacks keep working without anyone provisioning Resend.
The tests below pin that fallback plus a few render-correctness
properties of the Markdown attachment.
"""

from __future__ import annotations

import os

from website.server import email_notify


def test_dry_run_when_no_api_key(monkeypatch, capsys) -> None:
    monkeypatch.delenv("RESEND_API_KEY", raising=False)
    result = email_notify.send_report_ready(
        to="alice@example.org",
        run_id="run-1",
        slug="helm-sea",
        scoring={"risk_assessment": "low", "overall_summary": "ok"},
        raw_text="{}",
    )
    assert result.sent is True
    assert result.fallback is True
    assert result.provider_id is None
    captured = capsys.readouterr()
    assert "alice@example.org" in captured.err
    assert "RESEND_API_KEY unset" in captured.err


def test_markdown_report_includes_overall_summary() -> None:
    md = email_notify.render_markdown_report(
        slug="helm-sea",
        scoring={
            "risk_assessment": "medium",
            "overall_summary": "Concerns in input_content.",
            "dimensions": {
                "input_ontology": {
                    "score": 3,
                    "confidence": "high",
                    "justification": "Coverage is partial.",
                    "evidence_quotes": ["q1", "q2"],
                }
            },
            "remediation_suggestions": "Translate to Bahasa.",
        },
        raw_text="",
        link="https://example.org/run/abc",
    )
    assert "# Validity report (helm-sea)" in md
    assert "Concerns in input_content." in md
    assert "| input_ontology | 3 | high |" in md
    assert "Translate to Bahasa." in md
    assert "https://example.org/run/abc" in md


def test_markdown_report_falls_back_when_scoring_empty() -> None:
    md = email_notify.render_markdown_report(
        slug="x",
        scoring={},
        raw_text="this was not JSON",
        link="https://example.org/run/abc",
    )
    assert "could not be parsed as JSON" in md
    assert "this was not JSON" in md


def test_no_api_key_does_not_attempt_sdk_import(monkeypatch) -> None:
    """If RESEND_API_KEY is unset we must not blow up when the SDK is
    absent — the fallback never imports it."""
    monkeypatch.delenv("RESEND_API_KEY", raising=False)
    monkeypatch.setitem(os.environ, "WEBSITE_PUBLIC_URL", "http://localhost:5173")
    r = email_notify.send_report_ready(
        to="a@b.co", run_id="r", slug="s", scoring={}, raw_text="",
    )
    assert r.sent and r.fallback
