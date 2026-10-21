/**
 * Public MathDial source data and authored examples for the free walkthrough.
 * These labels are teaching examples, not an item-analysis model run or study.
 * Source records are unmodified; display formatting and judgments are additions.
 */
import sample from './mathdialSample.json'
import catalog from './genericItemCatalog.json'
import {
  DEMO_DEPLOYMENT_DESCRIPTION, DEMO_ELICITATION_SUMMARY, DEMO_GALLERY_ID, DEMO_SCORING,
} from './fixture'
import type { AnalysisRun, AnalysisSummary, Classifier, Item, Specification } from '../itemAnalysis/types'

export const DEMO_ITEM_ANALYSIS_PILOT_SIZE = 4

export const DEMO_ITEM_ANALYSIS_PROVENANCE = {
  title: 'MathDial — 10-dialogue walkthrough sample',
  source_url: 'https://huggingface.co/datasets/eth-nlped/mathdial/blob/acc3878459e0bd8c04ab840056572f0b8b1abe1f/test.jsonl',
  repo: 'eth-nlped/mathdial',
  revision: 'acc3878459e0bd8c04ab840056572f0b8b1abe1f',
  source_path: 'test.jsonl',
  source_route: 'Bundled directly from the public upstream MathDial repository at the revision below; this demo does not perform or claim a Data Bank match.',
  split: 'test',
  source_split_count: 599,
  source_file_sha256: '3ec54ee8ab921dc6191bf5e2ee766d4e7916b4264394eb17a6be9b3fe486e50b',
  license: 'CC BY 4.0',
  license_url: 'https://creativecommons.org/licenses/by/4.0/',
  license_source_url: 'https://huggingface.co/datasets/eth-nlped/mathdial/blob/acc3878459e0bd8c04ab840056572f0b8b1abe1f/README.md',
  citation: 'Jakub Macina, Nico Daheim, Sankalan Pal Chowdhury, Tanmay Sinha, Manu Kapur, Iryna Gurevych, and Mrinmaya Sachan (2023). MathDial: A Dialogue Tutoring Dataset with Rich Pedagogical Properties Grounded in Math Reasoning Problems.',
  paper_url: 'https://arxiv.org/abs/2305.14536',
  item_count: sample.items.length,
  item_unit: 'One complete published dialogue; problem qids can repeat across dialogues.',
  sample_description: 'The first 10 dialogues in the pinned test.jsonl (of 599 test dialogues), a convenience sample, not representative of MathDial or any student population. These are 10 dialogues covering 9 distinct problem qids, not the full benchmark.',
  label_provenance: 'Authored illustrative judgments for this walkthrough. They are not outputs from an item-analysis model run, expert-validated annotations, or study findings. No model calls are made.',
  changes: 'Original source records are preserved without edits. Display formatting, row-qualified item IDs, classification criteria, evidence selections, and illustrative judgments were added for this walkthrough.',
  student_provenance: 'MathDial pairs human teachers with LLM-simulated students; these are published dataset dialogues, not recordings of real students.',
  assessment_id: DEMO_GALLERY_ID,
} as const

export type DemoItemAnalysisProvenance = typeof DEMO_ITEM_ANALYSIS_PROVENANCE

export const DEMO_ITEM_ANALYSIS_CLASSIFIER_NAMES: Record<string, string> = {
  input_ontology: 'Input Ontology', input_content: 'Input Content',
  output_ontology: 'Output Ontology', output_content: 'Output Content',
}

const dimensions = DEMO_SCORING.dimensions as Record<string, { justification: string }>

const demoProfile = { item_count: sample.items.length, fields: Object.keys(sample.items[0].record), reference_answers: sample.items.filter(item => item.record.ground_truth).length }

const DEMO_CONTEXT = {
  deployment_requirements: [{ statement: DEMO_DEPLOYMENT_DESCRIPTION, source_ids: ['deployment_description.txt'] }, { statement: 'Curriculum-agnostic math errors are sufficient for evaluating pedagogical quality; Indian curriculum specifics are not required.', source_ids: ['elicitation_summary.md'] }],
  benchmark_evidence: [{ statement: 'The first bundled example contains a mathematical problem, a reference solution, and a tutoring conversation with teacher-move tags.', source_ids: ['sample/row-1'] }],
  prior_hypotheses: [],
  evidence_gaps: ['No independent target-teacher item judgments or complete scoring and annotation documentation are bundled.'],
}

export const DEMO_ITEM_ANALYSIS_SPEC: Specification = {
  schema_version: 'caliper_item_spec_v2', fixed_catalog_version: 'caliper_generic_items_v1',
  benchmark: 'mathdial', deployment: DEMO_DEPLOYMENT_DESCRIPTION,
  deployment_description: DEMO_DEPLOYMENT_DESCRIPTION,
  dataset_profile: demoProfile, semantic_validation: 'unreviewed',
  analysis_basis: 'benchmark_assessment', assessment_status: 'complete',
  source_roles: {
    'deployment_description.txt': 'deployment_requirement', 'elicitation_summary.md': 'deployment_requirement', 'demo_profile.json': 'dataset_profile',
    ...Object.fromEntries(Object.keys(dimensions).map(id => [`scoring.json#/dimensions/${id}`, 'prior_assessment'])),
    ...Object.fromEntries(sample.items.map(item => [`sample/row-${item.source_row}`, 'example_item'])),
  },
  classifiers: catalog.classifiers as Classifier[],
  input_category_inventory: {
    completeness: 'partial', completeness_source_ids: [],
    categories: [{ id: 'required_001', name: 'Curriculum-agnostic mathematical errors',
      definition: 'Mathematical-error tutoring scenarios for evaluating pedagogical quality; Indian curriculum specifics are not required.',
      source_ids: ['elicitation_summary.md'] }],
    evidence_gaps: ['The deployment evidence does not establish an exhaustive input-category inventory.'],
  },
  context_by_classifier: Object.fromEntries(catalog.classifiers.map(classifier => [classifier.id, {
    ...structuredClone(DEMO_CONTEXT),
    prior_hypotheses: [{ statement: dimensions[classifier.id].justification,
      source_ids: [`scoring.json#/dimensions/${classifier.id}`] }],
  }])),
  source_registry: {
    'deployment_description.txt': DEMO_DEPLOYMENT_DESCRIPTION,
    'elicitation_summary.md': DEMO_ELICITATION_SUMMARY,
    'demo_profile.json': demoProfile,
    ...Object.fromEntries(Object.entries(dimensions).map(([id, value]) => [`scoring.json#/dimensions/${id}`, value])),
    ...Object.fromEntries(sample.items.map(item => [`sample/row-${item.source_row}`, item.record])),
  },
}

type Label = NonNullable<Item['labels']>[string]
type SourceRecord = typeof sample.items[number]['record']
export type DemoItemAnalysisItem = Item & {
  source: { repo: string; revision: string; path: string; split: string; row_1based: number; row_sha256: string; qid: number; scenario: number }
  original_record: SourceRecord
  judgment_provenance: string
}

// Deliberately authored, fixed examples. No model or remote evaluation runs here.
// Each evidence excerpt is copied from the corresponding published record.
const examples: {
  task: string; taskEvidence: string; taskReason: string
  moves: string; moveEvidence: string
  answer: 0 | 1; answerEvidence: string; answerReason: string
  region: 1 | 2; regionEvidence: string
}[] = [
  {
    task: 'additive_reasoning', taskEvidence: 'The total number of spoons from Julia and her husband was 12+3=15 spoons.', taskReason: 'Recovering the starting number of spoons uses addition and subtraction.',
    moves: 'includes_telling', moveEvidence: 'Teacher: (telling)No, you need to add as she still has the spoons, 3 have just been used',
    answer: 0, answerEvidence: "Teacher: (generic)Yes, that's it", answerReason: 'The student states 10; the teacher supplies the operation and affirms the result without explicitly stating the final number.',
    region: 2, regionEvidence: 'Julia was preparing for a dinner party at her house, where she intended to serve stew.',
  },
  {
    task: 'additive_reasoning', taskEvidence: 'The bids on the desk rise by $50 each time and 3 other people each bid once.', taskReason: 'The task tracks repeated bid increments and adds them to the opening bid.',
    moves: 'includes_telling', moveEvidence: 'Teacher: (telling)200 + 150 + 150 is 500 not 350',
    answer: 1, answerEvidence: 'Teacher: (telling)No the answer is $500 as $200 + $150 + $150 is $500', answerReason: 'The teacher explicitly gives the final price of $500.',
    region: 1, regionEvidence: 'She accepts the opening bid of $200 and continues bidding until she wins.',
  },
  {
    task: 'percentages', taskEvidence: 'Karan borrowed $3,650 for five months at an interest rate of 10%.', taskReason: 'The task applies percentage interest before dividing the total repayment into instalments.',
    moves: 'focus_without_probing_or_telling', moveEvidence: 'Teacher: (focus)Slow down. What is £3650 x 0.1?',
    answer: 0, answerEvidence: 'The interest is $365 which then needs to be added to the amount borrowed before being dividing by the amount of months', answerReason: 'The teacher supplies an intermediate interest value and the next steps, but the student first states the final monthly payment of $803.',
    region: 1, regionEvidence: 'Teacher: (focus)Slow down. What is £3650 x 0.1?',
  },
  {
    task: 'additive_reasoning', taskEvidence: 'Josh starts with 3 balls and adds 1 ball each week for 4 weeks for a total of 3+4=7', taskReason: 'The task adds the weekly increases and subtracts the dropped balls.',
    moves: 'focus_without_probing_or_telling', moveEvidence: 'Teacher: (focus)And finally drops 3 making the total..',
    answer: 0, answerEvidence: 'Teacher: (focus)And finally drops 3 making the total..', answerReason: 'The teacher leaves the final value for the student, who replies “4 balls.”',
    region: 2, regionEvidence: 'Josh decides to take up juggling to perform at the school talent show a month in the future.',
  },
  {
    task: 'proportional_reasoning', taskEvidence: 'He bought 4 pounds of candy because 6 / 1.5 = 4', taskReason: 'The task works backwards from a unit price and half of the remaining change.',
    moves: 'focus_without_probing_or_telling', moveEvidence: 'Teacher: (focus)Slow down. He spents $2 on gumballs. You need to / this by 0.5 to calculate the change',
    answer: 0, answerEvidence: 'Teacher: (focus)Slow down. He spents $2 on gumballs. You need to / this by 0.5 to calculate the change', answerReason: 'The teacher provides a procedure for finding change; the student supplies the final four pounds of candy.',
    region: 1, regionEvidence: 'The candy costs $1.5 a pound.',
  },
  {
    task: 'additive_reasoning', taskEvidence: "Since the husband bought a package of five spoons, then Julia's package contained 15-5=10 spoons.", taskReason: 'This is a second dialogue about the same additive-reasoning problem as the first item, not an additional unique problem.',
    moves: 'includes_telling', moveEvidence: 'Teacher: (telling)The answer is 10',
    answer: 1, answerEvidence: 'Teacher: (telling)The answer is 10 could you try to use the information you have to get this', answerReason: 'The teacher explicitly states the final number 10; the criterion counts this regardless of earlier student responses.',
    region: 2, regionEvidence: 'Julia was preparing for a dinner party at her house, where she intended to serve stew.',
  },
  {
    task: 'proportional_reasoning', taskEvidence: 'There are 14/2 = 7 fish in each aquarium.', taskReason: 'The task interprets a factor of two and then divides the fish equally between the aquariums.',
    moves: 'probing_without_telling', moveEvidence: 'Teacher: (probing)You are almost there with you answer I think you need maybe one more step',
    answer: 0, answerEvidence: 'Teacher: (focus)14 is the total for both aquarium so how many would be in each if they are the sme', answerReason: 'The teacher asks for the equal split of 14 and does not explicitly state the final answer 7.',
    region: 2, regionEvidence: 'There are 4 snails in one aquarium and 32 snails in another aquarium.',
  },
  {
    task: 'proportional_reasoning', taskEvidence: 'Three total people can attend because 90 / 30 = 3', taskReason: 'The task divides a total budget by the cost per person and then removes the host from the friend count.',
    moves: 'includes_telling', moveEvidence: 'Teacher: (telling)Divide by 30 which is your total',
    answer: 1, answerEvidence: 'Teacher: (telling)90 divide by 30 means 3 people , given Morgan uses one place she can take 2 friends. Do you understand', answerReason: 'The teacher explicitly states that Morgan can take two friends.',
    region: 1, regionEvidence: "Morgan's dad said that she had $90 budgeted for her birthday party.",
  },
  {
    task: 'proportional_reasoning', taskEvidence: 'He started with 150 cards because 100 / (2/3) = 150', taskReason: 'The task combines a unit selling price with the fraction of a collection that was sold.',
    moves: 'includes_telling', moveEvidence: 'Teacher: (telling)If I tell you the answer is 150 cards can you work to this figure',
    answer: 1, answerEvidence: 'Teacher: (telling)If I tell you the answer is 150 cards can you work to this figure', answerReason: 'The teacher explicitly gives the final answer of 150 cards.',
    region: 1, regionEvidence: 'He has a collection of cards and plans to sell them for $1.5 each.',
  },
  {
    task: 'percentages', taskEvidence: 'First find what percentage of the candles explode: 100% - 99% = 1%', taskReason: 'The task combines two percentage conditions to count the candles with both defects.',
    moves: 'focus_without_probing_or_telling', moveEvidence: 'Teacher: (focus)rishi your method is correct.',
    answer: 0, answerEvidence: 'Teacher: (generic)excellent', answerReason: 'The teacher redirects the interpretation and affirms the student; only the student states the final answer of 25.',
    region: 2, regionEvidence: 'Marcy makes homemade candles that she markets as 99% guaranteed not to explode.',
  },
]

function judgment(label: Label['label'], evidence: string[], justification: string): Label {
  return { label, evidence, justification: `Illustrative judgment: ${justification}` }
}

export const DEMO_ITEM_ANALYSIS_ITEMS: DemoItemAnalysisItem[] = sample.items.map(({ source_row, source_row_sha256, record }, index) => {
  const example = examples[index]
  return {
    item_id: `mathdial:test:row-${String(source_row).padStart(4, '0')}:qid-${record.qid}:scenario-${record.scenario}`,
    content: `Problem\n${record.question}\n\nStudent profile (simulated)\n${record.student_profile}\n\nInitial incorrect solution\n${record.student_incorrect_solution}\n\nTeacher-described confusion\n${record.teacher_described_confusion}\n\nComplete published dialogue\n${record.conversation.replaceAll('|EOM|', '\n\n')}`,
    reference_answer: record.ground_truth,
    status: 'complete',
    source: {
      repo: DEMO_ITEM_ANALYSIS_PROVENANCE.repo, revision: DEMO_ITEM_ANALYSIS_PROVENANCE.revision,
      path: 'test.jsonl', split: 'test', row_1based: source_row, row_sha256: source_row_sha256,
      qid: record.qid, scenario: record.scenario,
    },
    original_record: record,
    judgment_provenance: DEMO_ITEM_ANALYSIS_PROVENANCE.label_provenance,
    labels: {
      input_ontology: { ...judgment('match', [example.taskEvidence], 'The item instantiates a mathematical-error tutoring scenario, a category established by the elicitation evidence. This match does not establish suitability in every dimension.'), matched_category_ids: ['required_001'], scope_exclusion_source_ids: [] },
      input_content: judgment('insufficient_evidence', [example.regionEvidence], 'The scenario and dialogue are visible, but the bundled evidence does not establish whether their particular dependencies conflict with the intended pedagogical construct. Foreign currency or names alone are not an issue.'),
      output_ontology: judgment('insufficient_evidence', [example.moveEvidence], 'Published teacher-move tags identify some output distinctions, but the applicable scoring criteria and their weighting are not sufficiently documented here for comparison with deployment needs.'),
      output_content: judgment('insufficient_evidence', [`Published self-correctness: ${record['self-correctness']}`], 'A source self-correctness rating and numerical solution are available, but documented target-teacher judgments or applicable annotation standards for pedagogical quality are absent. Population agreement cannot be inferred.'),
    },
  }
})

function summarize(classifier: Classifier, completed: Item[], total: number) {
  const labels = classifier.labels || []
  const counts: Record<string, number> = Object.fromEntries(labels.map(label => [label, 0]))
  let unknown = 0
  for (const item of completed) {
    const label = item.labels?.[classifier.id]?.label
    if (label === 'insufficient_evidence') unknown += 1
    if (label != null) counts[String(label)] = (counts[String(label)] || 0) + 1
  }
  const known = completed.length - unknown
  return {
    ...classifier, counts, valid_judgments: completed.length, determinate_judgments: known, insufficient_evidence: unknown, invalid: 0, errors: 0, pending: total - completed.length,
    ...(classifier.id === 'input_ontology' ? { category_counts: { required_001: completed.filter(item => item.labels?.input_ontology.matched_category_ids?.includes('required_001')).length } } : {}),
    percentages_among_valid: Object.fromEntries(Object.entries(counts).map(([label, count]) => [label, completed.length ? count / completed.length * 100 : null])),
  }
}

/** All counts describe only the bundled sample; callers never contact an API. */
export function buildDemoItemAnalysisRun(scope: 'pilot' | 'sample'): AnalysisRun {
  const total = DEMO_ITEM_ANALYSIS_ITEMS.length
  const completedCount = scope === 'pilot' ? DEMO_ITEM_ANALYSIS_PILOT_SIZE : total
  // Each replay gets independent records; exported fixtures are never mutated.
  const items = structuredClone(DEMO_ITEM_ANALYSIS_ITEMS).map((item, index) => {
    if (index >= completedCount) {
      item.status = 'pending'
      delete item.labels
    }
    return item
  })
  const completed = items.filter(item => item.status === 'complete')
  const spec = structuredClone(DEMO_ITEM_ANALYSIS_SPEC)
  const summary: AnalysisSummary = {
    schema_version: 'caliper_item_spec_v2', report_schema_version: 'caliper_item_report_v2', fixed_catalog_version: DEMO_ITEM_ANALYSIS_SPEC.fixed_catalog_version,
    experiment: { classifier_count: spec.classifiers.length, selected_items: completed.length, completed_item_classifier_judgments: completed.length * spec.classifiers.length, expected_item_classifier_judgments: completed.length * spec.classifiers.length },
    total_items: total, completed_items: completed.length, error_items: 0, pending_items: total - completed.length,
    complete_snapshot: scope === 'sample',
    classifiers: spec.classifiers.map(classifier => summarize(classifier, completed, total)),
    original_assessment: structuredClone(DEMO_SCORING.dimensions as NonNullable<AnalysisSummary['original_assessment']>),
    dataset: {
      ...DEMO_ITEM_ANALYSIS_PROVENANCE,
      scope: 'bundled_walkthrough_sample', full_benchmark: false, representative_sample: false,
      completed_dialogues: completed.length,
    },
    specification: {
      deployment_text_matches: true,
      note: 'Authored example criteria use the exact deployment from the original MathDial report. Input Form and Output Form remain benchmark-level judgments. The four fixed rubric classifiers use sourced context with explicit evidence gaps. These authored judgments illustrate a workflow and have not been validated as study findings.',
    },
  }
  return {
    run_id: 'demo-mathdial-items',
    assessment: {
      kind: 'gallery', id: DEMO_GALLERY_ID, benchmark: 'mathdial', benchmark_name: 'MathDial',
      deployment: DEMO_DEPLOYMENT_DESCRIPTION, elicitation_summary: DEMO_ELICITATION_SUMMARY,
      scoring: structuredClone(DEMO_SCORING),
    },
    status: scope === 'pilot' ? 'checkpoint' : 'complete',
    message: scope === 'pilot'
      ? `Showing authored judgments for ${completed.length} of ${total} bundled dialogues. Continue to reveal the rest of this sample.`
      : `Showing authored judgments for all ${total} bundled dialogues. This is not the full MathDial benchmark.`,
    example: {
      id: 'demo-mathdial-public-sample', title: DEMO_ITEM_ANALYSIS_PROVENANCE.title,
      benchmark_title: 'MathDial', assessment_title: 'Indian metropolitan tutoring deployment',
      description: DEMO_ITEM_ANALYSIS_PROVENANCE.sample_description, item_count: total,
      benchmark: 'mathdial', deployment: DEMO_DEPLOYMENT_DESCRIPTION,
      source_label: 'MathDial public test split — fixed 10-dialogue walkthrough sample',
      source_url: DEMO_ITEM_ANALYSIS_PROVENANCE.source_url, source_revision: DEMO_ITEM_ANALYSIS_PROVENANCE.revision,
      available: true, supplied_spec_available: true,
    },
    spec, summary, processed: completed.length, total, complete: completed.length, errors: 0, items,
    pagination: { page: 1, total_pages: 1 }, usage: { input_tokens: 0, output_tokens: 0 },
    can_continue: scope === 'pilot', scope: scope === 'pilot' ? 'pilot' : 'all',
  }
}
