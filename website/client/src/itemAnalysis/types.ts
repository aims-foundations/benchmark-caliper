export interface Example {
  id: string
  title: string
  benchmark_title?: string
  assessment_title?: string
  description: string
  item_count: number
  benchmark: string
  deployment: string
  source_label: string
  source_url?: string
  source_revision?: string
  unavailable_reason?: string
  available: boolean
  supplied_spec_available?: boolean
}

export interface Catalog { examples: Example[]; checkpoint_size: number }
export interface AssessmentReference { kind: 'run' | 'gallery' | 'direct'; id: string }
export interface DirectContext {
  benchmark: string
  deployment: string
  task_requirements: string
  answer_requirements: string
  validity_concerns?: string
}
export interface AssessmentContext extends AssessmentReference {
  benchmark: string
  benchmark_name?: string
  deployment: string
  elicitation_summary?: string
  scoring?: Record<string, unknown>
  benchmark_identity?: BenchmarkIdentity
  direct_context?: DirectContext
  assessment_status?: 'not_run'
  analysis_basis?: 'deployment_requirements'
}
export interface BenchmarkIdentity {
  name: string
  full_name: string | null
  aliases: string[]
  paper_urls: string[]
  source_urls: string[]
  year: string | null
  languages: string[]
  version: string | null
  evidence: Record<string, string>
}
export interface SourceCatalog {
  status: 'ready' | 'cached' | 'unavailable'
  message: string
  repo: string
  revision: string | null
  requires_confirmation: true
}
export interface AssessmentSource {
  id: string
  title: string
  benchmark: string
  item_count: number
  available: boolean
  source_label: string
  source_url?: string
  source_revision?: string
  unavailable_reason?: string
  version?: string | null
  split?: string | null
  testing_scope?: string | null
  match_reasons: string[]
  conflicts: string[]
  match_type: 'identifier' | 'exact_name' | 'related_name' | 'search'
  requires_confirmation: true
}
export interface SourceDiscovery {
  sources: AssessmentSource[]
  benchmark_identity: BenchmarkIdentity
  catalog: SourceCatalog
}
export interface AssessmentSetup extends SourceDiscovery {
  assessment: AssessmentContext
  checkpoint_size: number
  upload: { max_bytes: number; max_items: number; formats: string[] }
}
export type ConfirmedDataset = { benchmark_confirmed: true } & (
  { source_id: string; source_revision: string; items_file?: never } |
  { items_file: File; source_id?: never; source_revision?: never }
)
export interface RunAccess { run_id: string; run_secret: string }
export type SpecificationMode = 'generate' | 'provided'
export type RunScope = 'pilot' | 'all'
export type Artifact = 'spec' | 'items' | 'summary' | 'report' | 'review'

export interface Classifier {
  id: string
  component: string
  operation: 'multilabel' | 'judgment' | 'assignment' | 'flag' | 'ordinal'
  applicable: boolean
  na_reason?: string
  criterion?: string
  question?: string
  decision_rules?: string[]
  labels?: string[]
  response_contract?: Record<string, unknown>
  category_set?: string[]
  ordinal_anchors?: Record<string, string>
  positive_class?: string
  grounded_in?: string[]
  example_items?: string[]
}

export interface SourcedStatement { statement: string; source_ids: string[] }
export interface ClassifierContext {
  deployment_requirements: SourcedStatement[]
  benchmark_evidence: SourcedStatement[]
  prior_hypotheses: SourcedStatement[]
  evidence_gaps: string[]
}
export interface CategoryInventory {
  completeness: 'complete' | 'partial' | 'unknown'
  completeness_source_ids: string[]
  categories: { id: string; name: string; definition: string; source_ids: string[] }[]
  evidence_gaps: string[]
}
export interface Specification {
  schema_version?: string
  fixed_catalog_version?: string
  deployment_description?: string
  dataset_profile?: Record<string, unknown>
  semantic_validation?: string
  analysis_basis?: string
  assessment_status?: string
  input_category_inventory?: CategoryInventory
  context_by_classifier?: Record<string, ClassifierContext>
  source_registry?: Record<string, unknown>
  source_roles?: Record<string, string>
  benchmark: string
  deployment: string
  classifiers: Classifier[]
}

export interface ClassifierSummary extends Classifier {
  counts?: Record<string, number>
  known?: number
  unknown?: number
  invalid?: number
  errors?: number
  insufficient_evidence?: number
  valid_judgments?: number
  determinate_judgments?: number
  percentages_among_valid?: Record<string, number | null>
  category_counts?: Record<string, number>
  pending?: number
  percentages_among_known?: Record<string, number | null>
}

export interface OriginalAssessment {
  score?: number | null
  justification?: string
  reasoning?: string
  [key: string]: unknown
}

export interface AnalysisSummary {
  report_schema_version?: string
  schema_version?: string
  fixed_catalog_version?: string
  classifier_count?: number
  completed_judgments?: number
  expected_judgments?: number
  experiment?: {
    classifier_count: number
    selected_items: number
    completed_item_classifier_judgments: number
    expected_item_classifier_judgments: number
    [key: string]: unknown
  }
  total_items: number
  completed_items: number
  error_items: number
  pending_items: number
  complete_snapshot: boolean
  classifiers: ClassifierSummary[]
  original_assessment?: Record<string, OriginalAssessment | null>
  dataset?: Record<string, unknown>
  specification?: {
    note?: string
    deployment_text_matches?: boolean
    adjustments?: { field?: string; reason?: string }[]
  }
}

export interface Item {
  item_id: string
  content: unknown
  reference_answer: unknown
  status: string
  error?: string
  classifier_errors?: Record<string, string>
  labels?: Record<string, { label: string | number | null; evidence: string[]; justification: string; matched_category_ids?: string[]; scope_exclusion_source_ids?: string[] }>
}

export interface AnalysisRun {
  run_id: string
  created_at?: string
  updated_at?: string
  retention?: { automatic_expiry: boolean; expires_at: string | null }
  assessment?: AssessmentContext
  status: 'preparing' | 'generating' | 'ready' | 'running' | 'checkpoint' | 'complete' | 'cancelled' | 'failed'
  message: string
  example: Example
  spec: Specification | null
  summary: AnalysisSummary | null
  processed: number
  total: number
  complete: number
  errors: number
  completed_judgments?: number
  remaining_judgments?: Record<RunScope, number>
  items: Item[]
  pagination: { page: number; total_pages: number }
  usage: { input_tokens: number; output_tokens: number }
  model?: { provider: string; model_id: string; reasoning_effort: string }
  can_continue: boolean
  error?: string
  failure?: { stage: string; code: string; message: string } | null
  scope: RunScope | null
}
