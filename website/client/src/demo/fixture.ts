/* ============================================================
   Demo-mode fixture: a real expert-assessed MathDial run replayed
   as a scripted walkthrough so visitors can see the pipeline
   without supplying an Anthropic API key. Source: the curated
   `expert_1a429e941728__mathdial/india_urban_english_tutoring`
   assessment that ships with the release package.
   ============================================================ */

import scoringJson from './scoring.json'
import elicitationSummaryMd from './elicitation_summary.md?raw'

import type { Question } from '../api'

export const DEMO_SLUG = 'india_urban_english_tutoring'
export const DEMO_RUN_ID = 'demo-mathdial'
export const DEMO_BENCHMARK_LABEL = 'MathDial — India urban tutoring (demo)'

export const DEMO_DEPLOYMENT_DESCRIPTION =
  'Use case and domain: Deployment scenario: A GPT-4 model is implemented ' +
  "in a one-on-one tutoring session, where its responses are augmented " +
  "with a human tutor's input. The tutor evaluates the pedagogical quality " +
  'of the combined response, particularly in terms of how well it provides ' +
  'guidance. The goal is to assess whether the augmented GPT-4 responses ' +
  'are acceptable to the tutor.\n\n' +
  'Domain: Educational tutoring\n' +
  'Setting: Mobile application / enterprise software\n' +
  'Target population: High-end professional teacher teaching grade 1–8 in ' +
  'major metropolitan cities in India, such as Delhi and Mumbai, who is ' +
  'fluent in English.'

// Lightweight metadata, used as the `metadata` text bundled into the
// 2-questions event during the running phase. Mirrors what the real
// metadata-extraction step would produce.
export const DEMO_METADATA =
  '- name: mathdial\n' +
  '- full_name: MATHDIAL: A Dialogue Tutoring Dataset with Rich ' +
  'Pedagogical Properties Grounded in Math Reasoning Problems\n' +
  '- year: 2023\n' +
  '- domain: Math tutoring dialogues with pedagogical annotations\n' +
  '- languages: English\n' +
  '- primary_region: UNKNOWN\n' +
  '- input_modalities: text\n' +
  '- output_modalities: text'

export const DEMO_QUESTIONS: Question[] = [
  {
    id: 'Q1',
    dimension: 'IO',
    question:
      'For your Grade 1–8 teachers in Delhi and Mumbai, do the student ' +
      'mistake scenarios covered by the benchmark need to reflect the ' +
      'Indian curriculum (e.g., NCERT/CBSE topics, Indian arithmetic ' +
      'conventions like the lakhs/crores place-value system, or standard ' +
      'algorithms taught differently in Indian textbooks)? Or would ' +
      'curriculum-agnostic math errors be sufficient for evaluating ' +
      'pedagogical quality?',
  },
  {
    id: 'Q2',
    dimension: 'IC',
    question:
      "The benchmark's student-tutor conversations are drawn from a " +
      'particular linguistic and cultural context that may not reflect ' +
      'Indian classroom dynamics. For your professional teachers in ' +
      'Indian metros, would the depicted student mistakes, communication ' +
      'styles, or classroom interaction norms feel realistic — or do you ' +
      'expect meaningful differences (e.g., more teacher-directed ' +
      'correction styles, deference patterns, locally common ' +
      'misconceptions specific to Indian students)?',
  },
  {
    id: 'Q3',
    dimension: 'OO',
    question:
      'The benchmark scores pedagogical quality along a set of dimensions ' +
      "covering aspects such as guidance, tone, and actionability. For " +
      "your teachers evaluating whether an augmented GPT-4 response is " +
      "'acceptable,' which dimensions matter most — and are there " +
      'dimensions the benchmark may be missing that your teachers would ' +
      'actually judge responses on, such as alignment with the prescribed ' +
      'syllabus or appropriateness of formality?',
  },
  {
    id: 'Q4',
    dimension: 'OC',
    question:
      "The benchmark's ground-truth annotations were produced by " +
      'annotators from a general (likely non-Indian) pool. When your ' +
      'professional Indian teachers evaluate whether a tutoring response ' +
      'provides good guidance, do you expect their judgments to ' +
      'systematically differ — e.g., valuing more direct correction over ' +
      'Socratic probing, or prioritising exam-readiness over conceptual ' +
      'exploration — compared to what a Western educator might consider ' +
      'high-quality pedagogy?',
  },
]

// Expert answers, pre-filled into the AnswerForm so visitors see a worked
// example rather than blank textareas.
export const DEMO_EXPERT_ANSWERS: Record<string, string> = {
  Q1: 'Curriculum-agnostic math errors are sufficient for evaluating pedagogical quality.',
  Q2:
    'Western student–tutor datasets capture many universal conceptual ' +
    'mistakes, but the interaction style often differs from Indian metro ' +
    'classrooms. Indian students tend to be more brief, deferential, and ' +
    'less likely to verbalize reasoning; teachers may use more direct, ' +
    'exam-oriented correction rather than extended Socratic dialogue. ' +
    'Procedure-heavy learning patterns and language-related ' +
    'misunderstandings are underrepresented in Western data.',
  Q3:
    'For student mistake remediation, these eight dimensions are ' +
    "expected to be necessary and sufficient. The critical dimension is " +
    "'providing guidance.'",
  Q4: 'Yes — some differences due to the Indian cultural context, teaching style, and pedagogy.',
}

export const DEMO_ELICITATION_SUMMARY: string = elicitationSummaryMd

export const DEMO_SCORING: Record<string, unknown> = scoringJson as Record<
  string,
  unknown
>

// The "raw" Opus output the ScoringView's raw tab displays. Real runs
// stream the model's literal text; for the demo we hand it a pretty-printed
// JSON of the same scoring object.
export const DEMO_RAW_TEXT: string = JSON.stringify(scoringJson, null, 2)
