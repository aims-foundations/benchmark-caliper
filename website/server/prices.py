"""Per-model token prices in USD per million tokens.

Routes by model family (Haiku / Sonnet / Opus) so the table does not need
updating every time Anthropic releases a point version. Verify against
https://platform.claude.com/docs/en/about-claude/pricing whenever you
suspect drift; that page is authoritative.

Last verified: 2026-05-10 against the official pricing page. Numbers
match the listed Claude 4.x family rates:
  - Haiku 4.5:    $1 input / $5 output per MTok
  - Sonnet 4.6:   $3 input / $15 output per MTok
  - Opus 4.7:     $5 input / $25 output per MTok  (note: Opus was
                  re-priced significantly cheaper from the 4.1 era's
                  $15/$75; older versions of this file used the old
                  Opus rates and overstated scoring cost by ~3x.)

Web search is billed separately at $10 per 1000 searches and is not
modelled here — see anthropic_client.WEB_SEARCH_TOOL.

Opus 4.7 also uses a new tokenizer that may use up to ~35% more tokens
for the same input vs. earlier models. That's a usage effect, not a
price change, so it doesn't appear in this table.
"""

from __future__ import annotations

# (input_price_per_mtok, output_price_per_mtok) in USD.
PRICES_USD_PER_MTOK: dict[str, tuple[float, float]] = {
    "haiku":  (1.00,  5.00),
    "sonnet": (3.00, 15.00),
    "opus":   (5.00, 25.00),
}


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    """USD cost for one API call. Routes by model family substring.

    Returns 0.0 for unrecognized models so a missing entry never blocks a
    run — but callers should treat 0 as a signal to update this table.
    """
    family = _family(model)
    if family is None:
        return 0.0
    in_p, out_p = PRICES_USD_PER_MTOK[family]
    return (input_tokens * in_p + output_tokens * out_p) / 1_000_000


def _family(model: str) -> str | None:
    m = model.lower()
    if "haiku" in m:
        return "haiku"
    if "sonnet" in m:
        return "sonnet"
    if "opus" in m:
        return "opus"
    return None
