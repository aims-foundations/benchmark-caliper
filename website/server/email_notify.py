"""Send the 'your validity report is ready' email at the end of a run.

Uses Resend as the email provider. The choice rationale lives in DESIGN.md:
modern transactional API, single env var to configure, free tier covers v0,
scales to production volume on the same code path so we never have to swap
providers later.

Graceful fallback: if `RESEND_API_KEY` is not set, this module logs the email
payload to stderr instead of sending. That lets local Docker / CI / a fresh
clone work without anyone needing to provision credentials. In production
the env var is set and emails go out for real.

Configuration:
  - RESEND_API_KEY        provider credential (required to actually send)
  - RESEND_FROM           sender address; must be on a verified domain in
                          production. Default: onboarding@resend.dev (the
                          test sender Resend allows without verification).
  - WEBSITE_PUBLIC_URL    the public origin used to build the report link
                          in the email body. Default: http://localhost:5173
                          which matches docker-compose.yml.
"""

from __future__ import annotations

import base64
import html
import json
import os
import sys
from dataclasses import dataclass
from typing import Optional


def _env_default() -> dict[str, str]:
    return {
        "api_key": os.environ.get("RESEND_API_KEY", ""),
        "from_addr": os.environ.get(
            "RESEND_FROM", "Validity Analyzer <onboarding@resend.dev>"
        ),
        "site_url": os.environ.get(
            "WEBSITE_PUBLIC_URL", "http://localhost:5173"
        ).rstrip("/"),
    }


@dataclass
class SendResult:
    sent: bool
    provider_id: Optional[str]
    fallback: bool  # True if RESEND_API_KEY was unset and we logged instead
    error: Optional[str] = None


def send_report_ready(
    *,
    to: str,
    run_id: str,
    slug: str,
    scoring: dict,
    raw_text: str,
) -> SendResult:
    """Send the report-ready email with the score JSON and a Markdown report
    attached.

    Returns SendResult; callers persist `sent` + `provider_id` to the runs
    table via `logging_gate.mark_email_sent`. Never raises — provider
    failures degrade to a logged error so a flaky email service doesn't
    take down an otherwise-successful run.
    """
    env = _env_default()
    link = f"{env['site_url']}/run/{run_id}"
    subject = "Your validity analysis is ready"
    markdown_report = render_markdown_report(
        slug=slug, scoring=scoring, raw_text=raw_text, link=link
    )
    body_text = _plain_body(slug=slug, link=link, scoring=scoring)
    body_html = _html_body(slug=slug, link=link, scoring=scoring)

    md_filename = f"validity_report_{slug or run_id}.md"
    json_filename = f"validity_scoring_{slug or run_id}.json"
    json_blob = json.dumps(scoring, indent=2, ensure_ascii=False)

    if not env["api_key"]:
        _log_fallback(
            to=to,
            subject=subject,
            link=link,
            attachments=[md_filename, json_filename],
        )
        return SendResult(sent=True, provider_id=None, fallback=True)

    try:
        import resend  # type: ignore
    except ImportError as e:
        return SendResult(
            sent=False,
            provider_id=None,
            fallback=False,
            error=f"resend SDK not installed: {e}",
        )

    resend.api_key = env["api_key"]

    try:
        resp = resend.Emails.send(
            {
                "from": env["from_addr"],
                "to": [to],
                "subject": subject,
                "text": body_text,
                "html": body_html,
                "attachments": [
                    {
                        "filename": md_filename,
                        "content": base64.b64encode(
                            markdown_report.encode("utf-8")
                        ).decode("ascii"),
                    },
                    {
                        "filename": json_filename,
                        "content": base64.b64encode(
                            json_blob.encode("utf-8")
                        ).decode("ascii"),
                    },
                ],
            }
        )
    except Exception as e:
        return SendResult(
            sent=False,
            provider_id=None,
            fallback=False,
            error=f"{type(e).__name__}: {e}",
        )

    provider_id = None
    if isinstance(resp, dict):
        provider_id = resp.get("id") or resp.get("data", {}).get("id")
    return SendResult(sent=True, provider_id=provider_id, fallback=False)


def _log_fallback(
    *, to: str, subject: str, link: str, attachments: list[str]
) -> None:
    print(
        "[email_notify] RESEND_API_KEY unset — DRY RUN, would have sent:\n"
        f"  to: {to}\n"
        f"  subject: {subject}\n"
        f"  link: {link}\n"
        f"  attachments: {attachments}",
        file=sys.stderr,
    )


def _plain_body(*, slug: str, link: str, scoring: dict) -> str:
    summary = _short_summary(scoring)
    return (
        "Your validity analysis is ready.\n\n"
        f"Run: {slug}\n"
        f"View the full report online: {link}\n\n"
        f"{summary}\n\n"
        "Two files are attached: the rendered Markdown report and the raw "
        "scoring JSON. You can also delete this run's stored data anytime by "
        "opening the link above and clicking 'Delete from server'.\n"
    )


def _html_body(*, slug: str, link: str, scoring: dict) -> str:
    summary = html.escape(_short_summary(scoring))
    safe_link = html.escape(link, quote=True)
    safe_slug = html.escape(slug or "")
    return (
        "<p>Your validity analysis is ready.</p>"
        f"<p><strong>Run:</strong> <code>{safe_slug}</code></p>"
        f'<p><a href="{safe_link}">View the full report online</a></p>'
        f"<pre style=\"white-space:pre-wrap;font-family:inherit\">{summary}</pre>"
        "<p>Two files are attached: the rendered Markdown report and the raw "
        "scoring JSON. You can delete this run's stored data anytime by "
        f'opening the link above and clicking "Delete from server".</p>'
    )


def _short_summary(scoring: dict) -> str:
    """Pull a few headline fields out of the scoring JSON for the body."""
    parts: list[str] = []
    risk = scoring.get("risk_assessment")
    if isinstance(risk, str) and risk:
        parts.append(f"Risk assessment: {risk}")
    overall = scoring.get("overall_summary")
    if isinstance(overall, str) and overall:
        # Trim to a couple of sentences for the email body.
        trimmed = overall.strip()
        if len(trimmed) > 600:
            trimmed = trimmed[:600].rstrip() + "…"
        parts.append(trimmed)
    if not parts:
        parts.append(
            "Open the link to view per-dimension scores, justifications, "
            "and remediation suggestions."
        )
    return "\n\n".join(parts)


def render_markdown_report(
    *, slug: str, scoring: dict, raw_text: str, link: str
) -> str:
    """Render the scoring JSON as a self-contained Markdown document.

    Keeps the email attachment legible without needing the website. If
    `scoring` is empty (parsing failed upstream), falls back to embedding
    the raw model output so the user still sees something useful.
    """
    if not scoring:
        return (
            f"# Validity report ({slug})\n\n"
            f"View online: {link}\n\n"
            "The scoring model returned a response that could not be "
            "parsed as JSON. Raw output:\n\n"
            "```\n" + raw_text.strip() + "\n```\n"
        )

    lines: list[str] = [f"# Validity report ({slug})", ""]
    lines.append(f"View online: {link}")
    lines.append("")
    risk = scoring.get("risk_assessment")
    if isinstance(risk, str) and risk:
        lines.append(f"**Risk assessment:** {risk}")
        lines.append("")
    overall = scoring.get("overall_summary")
    if isinstance(overall, str) and overall:
        lines.append("## Overall summary")
        lines.append("")
        lines.append(overall.strip())
        lines.append("")

    dimensions = scoring.get("dimensions")
    if isinstance(dimensions, dict) and dimensions:
        lines.append("## Per-dimension scores")
        lines.append("")
        lines.append("| Dimension | Score | Confidence |")
        lines.append("|-----------|-------|------------|")
        for name, payload in dimensions.items():
            if not isinstance(payload, dict):
                continue
            score = payload.get("score", "—")
            conf = payload.get("confidence", "—")
            lines.append(f"| {name} | {score} | {conf} |")
        lines.append("")
        for name, payload in dimensions.items():
            if not isinstance(payload, dict):
                continue
            lines.append(f"### {name}")
            lines.append("")
            jstr = payload.get("justification")
            if isinstance(jstr, str) and jstr:
                lines.append(jstr.strip())
                lines.append("")
            quotes = payload.get("evidence_quotes")
            if isinstance(quotes, list) and quotes:
                lines.append("**Evidence quotes:**")
                lines.append("")
                for q in quotes:
                    if isinstance(q, str):
                        lines.append(f"- {q}")
                lines.append("")

    remediation = scoring.get("remediation_suggestions")
    if isinstance(remediation, str) and remediation:
        lines.append("## Remediation suggestions")
        lines.append("")
        lines.append(remediation.strip())
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
