/* ============================================================
   Display-time calibration of the Opus scoring output.

   Two pieces of context Sanmi flagged are computed here so the
   score table can surface them honestly:

   1. Confidence calibration (Issue 1, "Layer 2" safety net).
      The framework's own rule is that `high` confidence requires
      support from at least two evidence streams (verbatim quotes,
      web sources, dataset findings). Opus self-reports confidence
      and tends toward "high" even on a single stream. We recount
      the streams that actually carried evidence and cap the label
      accordingly, independent of what the model claimed:
        >=2 streams -> the model's label stands
         1 stream   -> capped at "medium"
         0 streams  -> capped at "low"
      This mirrors the framework's own definitions of medium/low.

   2. Priority weights (Issue 3, Fix A). The elicitation step
      assigns each of the six dimensions a HIGH / MODERATE / LOWER
      priority, but only as a markdown table in the elicitation
      summary. We parse it so the table can show a badge beside
      each score — a 5/5 on a LOWER dimension should not visually
      outweigh a 1/5 on a HIGH one.
   ============================================================ */

export type Confidence = 'high' | 'medium' | 'low'
export type Priority = 'HIGH' | 'MODERATE' | 'LOWER'

const CONFIDENCE_RANK: Record<Confidence, number> = {
  low: 0,
  medium: 1,
  high: 2,
}

/** The three evidence streams a dimension can draw on. */
interface EvidenceStreams {
  quotes: number
  web: number
  dataset: number
}

function len(value: unknown): number {
  return Array.isArray(value) ? value.filter((v) => v != null && v !== '').length : 0
}

export function evidenceStreams(dim: Record<string, unknown>): EvidenceStreams {
  return {
    quotes: len(dim.evidence_quotes),
    // Real runs and the gallery use evidence_web_sources; some older
    // fixtures used evidence_region_sources. Treat them as one stream.
    web: len(dim.evidence_web_sources) || len(dim.evidence_region_sources),
    dataset: len(dim.evidence_dataset),
  }
}

export interface CalibratedConfidence {
  /** Confidence label as the model reported it (if any). */
  reported: Confidence | null
  /** Label after applying the two-stream rule. */
  calibrated: Confidence
  /** How many of the three evidence streams actually carried evidence. */
  streamCount: number
  /** True when the rule pulled the label below what the model claimed. */
  downgraded: boolean
}

function asConfidence(value: unknown): Confidence | null {
  return value === 'high' || value === 'medium' || value === 'low'
    ? value
    : null
}

/**
 * Apply the framework's two-evidence-stream rule to one dimension's
 * self-reported confidence. Always returns a label, even when the model
 * omitted one (derived purely from stream count in that case).
 */
export function calibrateConfidence(
  dim: Record<string, unknown>,
): CalibratedConfidence {
  const reported = asConfidence(dim.confidence)
  const streams = evidenceStreams(dim)
  const streamCount = [streams.quotes, streams.web, streams.dataset].filter(
    (n) => n > 0,
  ).length

  // The ceiling the evidence can justify.
  const ceiling: Confidence =
    streamCount >= 2 ? 'high' : streamCount === 1 ? 'medium' : 'low'

  // Start from the model's claim when present, otherwise from the ceiling,
  // then clamp down to the ceiling. We never raise a cautious model up.
  const start = reported ?? ceiling
  const calibrated: Confidence =
    CONFIDENCE_RANK[start] > CONFIDENCE_RANK[ceiling] ? ceiling : start

  return {
    reported,
    calibrated,
    streamCount,
    downgraded: reported != null && calibrated !== reported,
  }
}

const PRIORITY_VALUES: Priority[] = ['HIGH', 'MODERATE', 'LOWER']

// Two-letter dimension codes used in the elicitation priority table.
const CODE_TO_KEY: Record<string, string> = {
  IO: 'input_ontology',
  IC: 'input_content',
  IF: 'input_form',
  OO: 'output_ontology',
  OC: 'output_content',
  OF: 'output_form',
}

function normalizePriority(raw: string): Priority | null {
  const upper = raw.trim().toUpperCase()
  if (upper === 'MEDIUM' || upper === 'MODERATE') return 'MODERATE'
  if (upper === 'LOW' || upper === 'LOWER') return 'LOWER'
  if (upper === 'HIGH') return 'HIGH'
  return null
}

/**
 * Parse the "Dimension Priority Weights" markdown table out of the
 * elicitation summary. Returns a map keyed by dimension key
 * (e.g. "input_content"). Returns an empty map if the table is absent
 * or unparseable — callers should treat that as "no priority known".
 */
export function parsePriorityWeights(
  elicitationSummary: string | undefined,
): Record<string, Priority> {
  const out: Record<string, Priority> = {}
  if (!elicitationSummary) return out

  for (const line of elicitationSummary.split('\n')) {
    // Match rows like: | IC | HIGH | rationale ... |
    const m = line.match(/^\s*\|\s*([A-Za-z]{2})\s*\|\s*([A-Za-z]+)\s*\|/)
    if (!m) continue
    const key = CODE_TO_KEY[m[1].toUpperCase()]
    const priority = normalizePriority(m[2])
    if (key && priority) out[key] = priority
  }
  return out
}

/** Human-facing label for a priority badge. */
export const PRIORITY_LABEL: Record<Priority, string> = {
  HIGH: 'High priority',
  MODERATE: 'Moderate priority',
  LOWER: 'Lower priority',
}

export { PRIORITY_VALUES, CONFIDENCE_RANK }
