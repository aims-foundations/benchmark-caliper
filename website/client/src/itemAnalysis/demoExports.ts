import { DEMO_ITEM_ANALYSIS_CLASSIFIER_NAMES, DEMO_ITEM_ANALYSIS_PILOT_SIZE, DEMO_ITEM_ANALYSIS_PROVENANCE } from '../demo/itemAnalysisFixture'
import { classifierName, classifierQuestion, labelName } from './Criteria'
import { dimensionAverages, dimensionStatistics } from './sixScoreSummary'
import type { AnalysisRun, Artifact } from './types'

export interface DemoExport {
  filename: string
  mimeType: string
  content: string
}

const FILE_NAMES: Record<Artifact, string> = {
  spec: 'classifier_spec.json', items: 'items.csv', summary: 'summary.json', report: 'report.html', review: 'review.csv',
}
const JUDGMENT_ORIGIN = 'authored walkthrough examples, not model outputs'
const DATASET_SCOPE = 'bundled demo sample only; not the full MathDial benchmark'

function plain(value: unknown): string {
  return typeof value === 'string' ? value : value == null ? '' : JSON.stringify(value)
}

function escapeHtml(value: unknown): string {
  return plain(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]!)
}

function csvCell(value: unknown): string {
  const text = plain(value)
  // Keep spreadsheet applications from interpreting source text as formulas.
  const safe = /^[\s]*[=+@-]/.test(text) ? `'${text}` : text
  return `"${safe.replaceAll('"', '""')}"`
}

function csv(rows: unknown[][]): string {
  return rows.map(row => row.map(csvCell).join(',')).join('\r\n') + '\r\n'
}

function metadata(run: AnalysisRun) {
  return {
    ...DEMO_ITEM_ANALYSIS_PROVENANCE,
    judgment_origin: JUDGMENT_ORIGIN,
    dataset_scope: DATASET_SCOPE,
    scope: run.scope === 'pilot' ? 'pilot' : run.scope === 'all' ? 'sample' : 'criteria',
    pilot_size: DEMO_ITEM_ANALYSIS_PILOT_SIZE,
    shown_items: run.complete,
    sample_items: run.total,
    completed_demo_sample: run.status === 'complete' && run.complete === run.total,
    model_calls: 0,
    schema_version: run.spec?.schema_version, rubric_version: run.spec?.rubric_version, analysis_type: run.analysis_type, fixed_catalog_version: run.spec?.fixed_catalog_version,
    classifier_count: run.spec?.classifiers.length || 0, item_classifier_judgments: run.complete ? run.summary?.experiment?.completed_item_classifier_judgments || 0 : 0,
    classifier_names: Object.fromEntries((run.spec?.classifiers || []).map(classifier => [classifier.id, classifierName(classifier.id)])),
  }
}

/** All artifacts are local walkthrough exports, with provenance in the file. */
export function buildDemoExport(artifact: Artifact, run: AnalysisRun): DemoExport {
  const sixScores = run.analysis_type === 'six_scores'
  const demo = metadata(run)
  const filename = `mathdial-demo-${FILE_NAMES[artifact]}`
  if (artifact === 'spec' || artifact === 'summary') {
    const summary = sixScores && run.summary ? { ...run.summary,
      classifiers: run.summary.classifiers.map(dimension => ({ ...dimension, mean_score: dimensionStatistics(dimension).mean })),
      dimensions: (run.summary.dimensions || run.summary.classifiers).map(dimension => ({ ...dimension, mean_score: dimensionStatistics(dimension).mean })),
    } : run.summary
    const payload = artifact === 'spec' ? { demo, specification: run.spec } : { ...summary, demo }
    return { filename, mimeType: 'application/json;charset=utf-8', content: JSON.stringify(payload, null, 2) + '\n' }
  }

  if (artifact === 'items' || artifact === 'review') {
    const commonHeaders = ['schema_version', 'fixed_catalog_version', 'judgment_origin', 'dataset_scope', 'sample_items', 'shown_items', 'scope', 'source_revision', 'source_url', 'license', 'source_provenance']
    const common = [demo.schema_version, demo.fixed_catalog_version, demo.judgment_origin, demo.dataset_scope, demo.sample_items, demo.shown_items, demo.scope,
      demo.revision, demo.source_url, demo.license, JSON.stringify(DEMO_ITEM_ANALYSIS_PROVENANCE)]
    const rows: unknown[][] = []
    if (artifact === 'items') {
      rows.push(['item_id', 'content', 'reference_answer', 'status', sixScores ? 'authored_example_scores' : 'authored_example_labels', ...commonHeaders])
      for (const item of run.items) rows.push([item.item_id, item.content, item.reference_answer,
        item.status === 'complete' ? 'authored example shown' : 'pending after pilot', item.dimensions || item.labels || {}, ...common])
    } else if (sixScores) {
      rows.push(['item_id', 'content', 'reference_answer', 'dimension', 'question', 'ordinal_anchors', 'source_registry', 'human_score', 'human_justification', 'human_evidence', 'human_information_gaps', ...commonHeaders])
      for (const item of run.items.filter(item => item.status === 'complete')) for (const dimension of run.spec?.classifiers || []) rows.push([item.item_id, item.content, item.reference_answer, dimension.id, dimension.question, dimension.ordinal_anchors, run.spec?.source_registry, '', '', '', '', ...common])
    } else {
      rows.push(['item_id', 'content', 'reference_answer', 'classifier_id', 'question', 'decision_rules', 'allowed_labels', 'context', 'input_category_inventory', 'source_registry', 'human_label', 'human_matched_category_ids', 'human_scope_exclusion_source_ids', 'human_evidence', 'human_justification', ...commonHeaders])
      for (const item of run.items.filter(item => item.status === 'complete')) for (const classifier of run.spec?.classifiers || []) {
        if (classifier.applicable) rows.push([item.item_id, item.content, item.reference_answer, classifier.id, classifierQuestion(classifier), classifier.decision_rules, classifier.labels, run.spec?.context_by_classifier?.[classifier.id], run.spec?.input_category_inventory, run.spec?.source_registry, '', '', '', '', '', ...common])
      }
    }
    return { filename, mimeType: 'text/csv;charset=utf-8', content: csv(rows) }
  }

  const criteria = (run.spec?.classifiers || []).map(classifier => `<li><strong>${escapeHtml(classifierName(classifier.id, DEMO_ITEM_ANALYSIS_CLASSIFIER_NAMES))}</strong>: ${escapeHtml(classifier.applicable ? classifierQuestion(classifier) : classifier.na_reason)}</li>`).join('')
  const selected = run.summary?.experiment?.selected_items ?? run.total
  const evaluated = run.summary?.experiment?.selected_completed_items ?? run.summary?.completed_items ?? run.complete
  const averages = sixScores ? `<h2>Average item scores</h2><p>${evaluated} of ${selected} selected items evaluated, from ${run.total} items in this bundled demo sample. Each mean uses numeric authored scores for that dimension; Unknown, failed, and pending items are excluded. Original benchmark scores assess the benchmark as a whole.</p><div class="table-scroll"><table><thead><tr><th>Dimension</th><th>Item average</th><th>Items included</th><th>Benchmark score</th></tr></thead><tbody>${dimensionAverages(run).map(dimension => `<tr><th>${escapeHtml(classifierName(dimension.id))}</th><td>${dimension.mean === null ? 'Unknown (no numeric scores)' : `${dimension.mean.toFixed(2)} / 5`}</td><td>${dimension.known} numeric · ${dimension.unknown} Unknown</td><td>${escapeHtml(dimension.benchmark)}</td></tr>`).join('')}</tbody></table></div>` : ''
  const distributions = (run.summary?.classifiers || []).filter(classifier => classifier.applicable).map(classifier => `<section><h3>${escapeHtml(classifierName(classifier.id, DEMO_ITEM_ANALYSIS_CLASSIFIER_NAMES))}</h3><p>${classifier.known ?? classifier.determinate_judgments ?? 0} sufficient evidence · ${classifier.insufficient_evidence ?? classifier.unknown ?? 0} insufficient evidence · ${classifier.pending || 0} pending examples.</p><ul>${Object.entries(classifier.counts || {}).map(([label, count]) => `<li>${escapeHtml(labelName(classifier, label))}: ${count} (${(classifier.percentages_among_known?.[label] ?? classifier.percentages_among_valid?.[label])?.toFixed(1) ?? '—'}%)</li>`).join('')}</ul></section>`).join('')
  const items = run.items.map(item => `<article><h3>${escapeHtml(item.item_id)}</h3><pre>${escapeHtml(item.content)}</pre><p><strong>Reference answer:</strong> ${escapeHtml(item.reference_answer)}</p>${item.status !== 'complete' ? '<p>Pending after pilot review.</p>' : (run.spec?.classifiers || []).filter(classifier => classifier.applicable).map(classifier => {
    const dimension = item.dimensions?.[classifier.id]
    if (dimension) return `<h4>${escapeHtml(classifierName(classifier.id))}: ${dimension.score === null ? 'Unknown' : `${dimension.score} / 5`}</h4><p>${escapeHtml(dimension.justification)}</p><h5>Evidence</h5><ul>${dimension.evidence.map(value => `<li>${escapeHtml(value)}</li>`).join('')}</ul><h5>Missing information</h5><ul>${dimension.information_gaps.map(value => `<li>${escapeHtml(value)}</li>`).join('')}</ul>`
    const judgment = item.labels?.[classifier.id]
    return `<h4>${escapeHtml(classifierName(classifier.id, DEMO_ITEM_ANALYSIS_CLASSIFIER_NAMES))}: ${escapeHtml(judgment ? labelName(classifier, judgment.label) : 'Unknown')}</h4><p>${escapeHtml(judgment?.justification)}</p>${judgment?.matched_category_ids ? `<p>Matched categories: ${escapeHtml(judgment.matched_category_ids.join(', ') || 'None')}</p>` : ''}<ul>${(judgment?.evidence || []).map(evidence => `<li>${escapeHtml(evidence)}</li>`).join('')}</ul>`
  }).join('')}</article>`).join('')
  const content = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MathDial demo item analysis</title>
<style>body{font:16px/1.6 system-ui,sans-serif;max-width:960px;margin:3rem auto;padding:0 1.5rem;color:#292522}h1,h2,h3,h4{line-height:1.25}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit;background:#f6f4f0;padding:1rem}article,section{border-top:1px solid #ddd;padding-top:1rem;margin-top:1.5rem}a{overflow-wrap:anywhere}.table-scroll{overflow-x:auto}table{width:100%;border-collapse:collapse}th,td{padding:.6rem;border-bottom:1px solid #ddd;text-align:left}</style></head>
<body><h1>MathDial demo item analysis</h1><p><strong>${run.status === 'complete' ? 'Full demo sample' : 'Demo pilot results'}: ${run.complete} of ${run.total} bundled item judgments shown.</strong></p>
<p>These are ${escapeHtml(JUDGMENT_ORIGIN)}. Counts and percentages describe the ${escapeHtml(DATASET_SCOPE)}. No model calls were made.</p>
<h2>Source and judgment provenance</h2><p>${escapeHtml(demo.citation)}</p><p><a href="${escapeHtml(demo.source_url)}">Pinned MathDial source</a> · <a href="${escapeHtml(demo.license_url)}">${escapeHtml(demo.license)}</a></p><p>${escapeHtml(demo.sample_description)}</p><p>${escapeHtml(demo.label_provenance)}</p><pre>${escapeHtml(JSON.stringify(demo, null, 2))}</pre>
<h2>Deployment context</h2><pre>${escapeHtml(run.spec?.deployment)}</pre><h2>${sixScores ? 'Six-dimension rubric' : 'Fixed classifier questions'}</h2><ul>${criteria}</ul><details><summary>Full fixed rules and sourced context</summary><pre>${escapeHtml(JSON.stringify(run.spec, null, 2))}</pre></details>
${averages}<h2>Bundled sample summary</h2><p>${sixScores ? 'Percentages use numeric authored scores. Unknown, failed, and pending assessments are counted separately.' : 'Percentages use all valid authored example judgments, including insufficient evidence. Operational failures and pending examples are excluded from the denominator.'} No issue identified does not establish benchmark validity. A dash means there are no known labels.</p>${distributions}<h2>Original benchmark assessment</h2><p>Original benchmark-level scores are unchanged by these example item judgments.</p><pre>${escapeHtml(JSON.stringify(run.summary?.original_assessment || {}, null, 2))}</pre>
<h2>Example judgments</h2>${items}</body></html>`
  return { filename, mimeType: 'text/html;charset=utf-8', content }
}
