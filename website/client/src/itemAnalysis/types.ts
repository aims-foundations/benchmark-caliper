export interface Example {
  id: string
  title: string
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
export interface RunAccess { run_id: string; run_secret: string }
export type SpecificationMode = 'generate' | 'provided'
export type RunScope = 'pilot' | 'all'
export type Artifact = 'spec' | 'items' | 'summary' | 'report' | 'review'

export interface Classifier {
  id: string
  component: string
  operation: 'assignment' | 'flag' | 'ordinal'
  applicable: boolean
  na_reason?: string
  criterion: string
  category_set?: string[]
  ordinal_anchors?: Record<string, string>
  positive_class?: string
  grounded_in?: string[]
  example_items?: string[]
}

export interface Specification {
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
  content: string | null
  reference_answer: unknown
  status: string
  error?: string
  labels?: Record<string, { label: string | number | null; evidence: string[]; justification: string }>
}

export interface AnalysisRun {
  run_id: string
  status: 'preparing' | 'generating' | 'ready' | 'running' | 'checkpoint' | 'complete' | 'cancelled' | 'failed'
  message: string
  example: Example
  spec: Specification | null
  summary: AnalysisSummary | null
  processed: number
  total: number
  complete: number
  errors: number
  items: Item[]
  pagination: { page: number; total_pages: number }
  usage: { input_tokens: number; output_tokens: number }
  can_continue: boolean
  error?: string
  scope: RunScope | null
}
