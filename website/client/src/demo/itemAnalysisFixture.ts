/**
 * Public MathDial source data and authored examples for the free walkthrough.
 * These labels are teaching examples, not an item-analysis model run or study.
 * Source records are unmodified; display formatting and judgments are additions.
 */
import sample from './mathdialSample.json'
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
  'IO.task_category': 'Mathematical task',
  'OO.output_category': 'Published teacher moves',
  'OO.value_encoding': 'Teacher answer disclosure',
  'IC.region_fit': 'Regional context cues',
  'OC.label_contestability': 'Target teacher agreement',
}

export const DEMO_ITEM_ANALYSIS_SPEC: Specification = {
  benchmark: 'mathdial',
  deployment: DEMO_DEPLOYMENT_DESCRIPTION,
  classifiers: [
    {
      id: 'IO.task_category', component: 'input_ontology', operation: 'assignment', applicable: true,
      criterion: 'Assign the main mathematical task in the problem: additive reasoning (addition/subtraction, including repeated additions), proportional reasoning (rates, fractions, equal sharing, or unit costs), or percentages (including percentage interest). If categories overlap, prefer percentages, then proportional reasoning. This describes task coverage, not grade suitability or teaching quality.',
      category_set: ['additive_reasoning', 'proportional_reasoning', 'percentages'],
      grounded_in: ['Original Input Ontology assessment: the deployment accepts curriculum-agnostic mathematical errors. These broad example categories summarize this small sample; they do not replace the benchmark taxonomy.'],
    },
    {
      id: 'OO.output_category', component: 'output_ontology', operation: 'assignment', applicable: true,
      criterion: 'Summarize the teacher-move tags already published inside this dialogue. Use includes_telling if any Teacher turn is tagged (telling); otherwise use probing_without_telling if any is tagged (probing); otherwise use focus_without_probing_or_telling if any is tagged (focus). Unknown if the required tags are missing. These are descriptive categories, not a ranking of acceptable teaching styles.',
      category_set: ['includes_telling', 'probing_without_telling', 'focus_without_probing_or_telling'],
      grounded_in: ['Original Output Ontology assessment: the deployment prioritizes providing guidance and may accept direct correction. Inspecting the published move categories exposes this choice without declaring one style universally better.'],
    },
    {
      id: 'OO.value_encoding', component: 'output_ontology', operation: 'flag', applicable: true,
      criterion: 'Flag 1 when a teacher explicitly states the final numerical answer anywhere in the dialogue, even after the student has reached it. Use 0 when the complete teacher dialogue contains no explicit final answer. Intermediate values, hints, and affirmation alone do not count. This identifies examples to discuss with the tutor; it does not establish premature disclosure or unacceptable guidance.',
      positive_class: 'teacher_explicitly_states_final_answer',
      grounded_in: ['Original Output Ontology assessment: MathDial values guidance over telling; the deployment may allow more direct correction. An explicit answer is an observable discussion point, not proof of a regional mismatch.'],
    },
    {
      id: 'IC.region_fit', component: 'input_content', operation: 'ordinal', applicable: true,
      criterion: 'Record only observable regional context cues in the problem and dialogue. Use 1 for explicit non-Indian currency or measurement conventions; 3 for an explicitly stated Indian setting without conflicting cues; otherwise use 2 when the region is unspecified. Names alone do not establish region. This narrow context check does not measure classroom interaction norms, student ability, cultural familiarity, or overall deployment fit.',
      ordinal_anchors: { '1': 'Explicit non-Indian currency or units', '2': 'Region unspecified', '3': 'Explicit Indian setting' },
      grounded_in: ['Original Input Content assessment flags currency/context and simulated interaction style. This example checks visible context cues only; the original concerns about interaction style require separate review.'],
    },
    {
      id: 'OC.label_contestability', component: 'output_content', operation: 'flag', applicable: true,
      criterion: 'Flag 1 only when published item evidence documents disagreement from the deployment’s Indian metropolitan Grade 1–8 teachers about whether this tutoring exchange is acceptable; use 0 only for documented agreement from that target group. Return Unknown if target-group evaluation is absent. The source self-correctness rating and the presence of an Indian-sounding name do not establish local acceptance.',
      positive_class: 'documented_target_teacher_disagreement',
      grounded_in: ['Original Output Content assessment: agreement from the deployment’s target teachers is not disaggregated. These source rows have no target-group acceptability judgments, so all examples remain Unknown on this criterion.'],
    },
  ],
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
      'IO.task_category': judgment(example.task, [example.taskEvidence], example.taskReason),
      'OO.output_category': judgment(example.moves, [example.moveEvidence], example.moves === 'includes_telling'
        ? 'At least one published teacher turn has a (telling) tag. The category reports the source tags, not a new assessment of teaching quality.'
        : example.moves === 'probing_without_telling'
          ? 'The published dialogue includes a (probing) tag and no (telling) tag.'
          : 'The published dialogue includes (focus) tags, with neither (probing) nor (telling) tags. A tag does not by itself establish how directive the utterance is.'),
      'OO.value_encoding': judgment(example.answer, [example.answerEvidence], example.answerReason),
      'IC.region_fit': judgment(example.region, [example.regionEvidence], example.region === 1
        ? 'Explicit currency or unit conventions provide a concrete context cue to discuss for the Indian deployment. This does not establish unfamiliarity or unsuitability for any learner.'
        : 'The setting has no explicit regional marker under this criterion. The names and topic do not establish Indian relevance, and region-unspecified is not a positive fit finding.'),
      'OC.label_contestability': judgment(null, [`Published self-correctness: ${record['self-correctness']}`], 'The record has a teacher self-correctness rating but no identified evaluation by the target Indian metropolitan teacher group. Local agreement or disagreement cannot be inferred, so this is Unknown.'),
    },
  }
})

function summarize(classifier: Classifier, completed: Item[], total: number) {
  const categories = classifier.category_set || (classifier.operation === 'flag' ? ['0', '1'] : Object.keys(classifier.ordinal_anchors || {}))
  const counts: Record<string, number> = Object.fromEntries(categories.map(category => [category, 0]))
  let unknown = 0
  for (const item of completed) {
    const label = item.labels?.[classifier.id]?.label
    if (label === null || label === undefined) unknown += 1
    else counts[String(label)] = (counts[String(label)] || 0) + 1
  }
  const known = completed.length - unknown
  return {
    ...classifier, counts, known, unknown, invalid: 0, errors: 0, pending: total - completed.length,
    percentages_among_known: Object.fromEntries(Object.entries(counts).map(([label, count]) => [label, known ? count / known * 100 : null])),
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
      note: 'Authored example criteria use the exact deployment from the original MathDial report. Input Form and Output Form remain benchmark-level judgments. These five checks illustrate a workflow, not a complete operationalization of the original report or a newly validated instrument.',
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
