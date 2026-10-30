import type { AdaptiveReview, PreparedPackage } from './api'

type Artifact = { filename: string; bytes: number; sha256?: string }
export interface ConstructionExample {
  id: string; title: string; description: string; run_id: string; result_state: string
  assessed_count: number; selected_count: number; coverage_complete: boolean
  artifacts: { report: Artifact; summary_report?: Artifact; items: Artifact; results: Artifact; package: Artifact & PreparedPackage }
}
export interface ConstructionItemSummary {
  item_id: string; index: number; question_preview: string; preview_kind?: 'question' | 'decision' | 'unavailable'; status: 'complete' | 'error'
  gate: 'pass' | 'fail' | 'unresolved' | null; matched_facet_ids: string[]; sources: string[]
  selected: boolean; initial: boolean; quality_score: number | null
}
export interface ConstructionComposition {
  selected_count: number
  sources: { name: string; count: number; percentage: number }[]
  unknown_source_count: number
  tasks: { facet_id: string; label: string; count: number }[]
  coverage: { requirement_index: number; label: string; minimum_items: number | null; selected_count: number; shortfall: number | null }[]
  question_text: { available_count: number; distinct_count: number; missing_count: number; overlaps: { item_ids: string[] }[] }
  formats: { counts: { label: string; count: number }[]; unknown_count: number; basis: string | null }
}
export interface ConstructionSnapshot { entry: ConstructionExample; review: AdaptiveReview; items: ConstructionItemSummary[]; composition?: ConstructionComposition }
