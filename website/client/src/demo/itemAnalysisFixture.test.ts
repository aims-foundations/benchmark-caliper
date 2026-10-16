import { describe, expect, it } from 'vitest'
import { DEMO_DEPLOYMENT_DESCRIPTION, DEMO_GALLERY_ID, DEMO_SCORING } from './fixture'
import {
  buildDemoItemAnalysisRun, DEMO_ITEM_ANALYSIS_ITEMS, DEMO_ITEM_ANALYSIS_PILOT_SIZE,
  DEMO_ITEM_ANALYSIS_PROVENANCE, DEMO_ITEM_ANALYSIS_SPEC,
} from './itemAnalysisFixture'

describe('free MathDial item walkthrough fixture', () => {
  it('attributes the exact public source and distinguishes original records from authored examples', () => {
    const provenance = DEMO_ITEM_ANALYSIS_PROVENANCE
    expect(provenance.repo).toBe('eth-nlped/mathdial')
    expect(provenance.revision).toBe('acc3878459e0bd8c04ab840056572f0b8b1abe1f')
    expect(provenance.source_url).toContain(`/blob/${provenance.revision}/test.jsonl`)
    expect(provenance.source_file_sha256).toBe('3ec54ee8ab921dc6191bf5e2ee766d4e7916b4264394eb17a6be9b3fe486e50b')
    expect(provenance.license).toBe('CC BY 4.0')
    expect(provenance.citation).toContain('Jakub Macina')
    expect(provenance.changes).toContain('Original source records are preserved without edits')
    expect(provenance.student_provenance).toContain('LLM-simulated students')
    expect(provenance.label_provenance).toContain('Authored illustrative judgments')
    expect(provenance.sample_description).toContain('not representative')
    expect(provenance.source_split_count).toBe(599)
    expect(provenance.source_route).toContain('does not perform or claim a Data Bank match')
  })

  it('keeps complete source dialogues and distinct IDs for repeated problem qids', () => {
    expect(DEMO_ITEM_ANALYSIS_ITEMS).toHaveLength(10)
    expect(new Set(DEMO_ITEM_ANALYSIS_ITEMS.map(item => item.item_id)).size).toBe(10)
    expect(new Set(DEMO_ITEM_ANALYSIS_ITEMS.map(item => item.source.qid)).size).toBe(9)
    for (const [index, item] of DEMO_ITEM_ANALYSIS_ITEMS.entries()) {
      expect(item.source.row_1based).toBe(index + 1)
      expect(item.source.row_sha256).toMatch(/^[a-f0-9]{64}$/)
      expect(item.source.qid).toBe(item.original_record.qid)
      expect(item.source.scenario).toBe(item.original_record.scenario)
      expect(item.source.path).toBe('test.jsonl')
      expect(item.source.revision).toBe(DEMO_ITEM_ANALYSIS_PROVENANCE.revision)
      expect(item.item_id).toContain(`qid-${item.original_record.qid}`)
      expect(item.content).toContain(item.original_record.question)
      expect(item.content).toContain(item.original_record.conversation.replaceAll('|EOM|', '\n\n'))
      expect(item.reference_answer).toBe(item.original_record.ground_truth)
      for (const judgment of Object.values(item.labels || {})) {
        expect(judgment.justification).toMatch(/^Illustrative judgment:/)
        for (const evidence of judgment.evidence) {
          if (evidence.startsWith('Published self-correctness: ')) {
            expect(evidence).toBe(`Published self-correctness: ${item.original_record['self-correctness']}`)
          } else {
            // Evidence is a verbatim excerpt, not a fabricated quote or paraphrase.
            expect(Object.values(item.original_record).some(value => typeof value === 'string' && value.includes(evidence))).toBe(true)
          }
        }
      }
    }
  })

  it('reuses the original deployment, six scores, and assessment reference exactly', () => {
    const run = buildDemoItemAnalysisRun('sample')
    expect(DEMO_ITEM_ANALYSIS_SPEC.deployment).toBe(DEMO_DEPLOYMENT_DESCRIPTION)
    expect(run.assessment?.deployment).toBe(DEMO_DEPLOYMENT_DESCRIPTION)
    expect(run.assessment?.id).toBe(DEMO_GALLERY_ID)
    expect(run.assessment?.scoring).toEqual(DEMO_SCORING)
    expect(run.summary?.original_assessment).toEqual(DEMO_SCORING.dimensions)
    expect(run.spec?.classifiers.map(classifier => classifier.component)).toEqual([
      'input_ontology', 'output_ontology', 'output_ontology', 'input_content', 'output_content',
    ])
    expect(run.summary?.specification?.note).toContain('Input Form and Output Form remain benchmark-level')
  })

  it('reveals four pilot judgments while keeping the six remaining dialogues pending', () => {
    const pilot = buildDemoItemAnalysisRun('pilot')
    expect(DEMO_ITEM_ANALYSIS_PILOT_SIZE).toBe(4)
    expect(pilot.status).toBe('checkpoint')
    expect(pilot.total).toBe(10)
    expect(pilot.complete).toBe(4)
    expect(pilot.can_continue).toBe(true)
    expect(pilot.summary?.pending_items).toBe(6)
    expect(pilot.summary?.complete_snapshot).toBe(false)
    expect(pilot.items.filter(item => item.status === 'pending')).toHaveLength(6)
    expect(pilot.items.slice(4).every(item => item.labels === undefined)).toBe(true)
    for (const classifier of pilot.summary!.classifiers) {
      expect(classifier.known! + classifier.unknown!).toBe(4)
      expect(classifier.pending).toBe(6)
    }
  })

  it('computes full-sample counts only from the bundled authored labels', () => {
    const run = buildDemoItemAnalysisRun('sample')
    expect(run.status).toBe('complete')
    expect(run.complete).toBe(10)
    expect(run.summary?.pending_items).toBe(0)
    expect(run.summary?.dataset?.full_benchmark).toBe(false)
    expect(run.summary?.dataset?.representative_sample).toBe(false)
    for (const classifier of run.summary!.classifiers) {
      const observed: Record<string, number> = Object.fromEntries(Object.keys(classifier.counts!).map(key => [key, 0]))
      let unknown = 0
      for (const item of run.items) {
        const label = item.labels![classifier.id].label
        if (label === null) unknown += 1
        else observed[String(label)] += 1
      }
      expect(classifier.counts).toEqual(observed)
      expect(classifier.unknown).toBe(unknown)
      expect(classifier.known).toBe(10 - unknown)
      for (const [label, count] of Object.entries(observed)) {
        expect(classifier.percentages_among_known![label]).toBe(unknown === 10 ? null : count / (10 - unknown) * 100)
      }
    }
    const byId = Object.fromEntries(run.summary!.classifiers.map(classifier => [classifier.id, classifier]))
    expect(byId['IO.task_category'].counts).toEqual({ additive_reasoning: 4, proportional_reasoning: 4, percentages: 2 })
    expect(byId['OO.value_encoding'].counts).toEqual({ '0': 6, '1': 4 })
    expect(byId['IC.region_fit'].counts).toEqual({ '1': 5, '2': 5, '3': 0 })
    expect(byId['OC.label_contestability'].known).toBe(0)
    expect(byId['OC.label_contestability'].unknown).toBe(10)
    expect(byId['OC.label_contestability'].percentages_among_known).toEqual({ '0': null, '1': null })
  })

  it('replays without altering the fixture and reports no paid or model-generated run', () => {
    const pilot = buildDemoItemAnalysisRun('pilot')
    pilot.items[0].labels!['IO.task_category'].label = 'edited'
    pilot.spec!.classifiers[0].criterion = 'edited'
    const replay = buildDemoItemAnalysisRun('sample')
    expect(replay.items[0].labels!['IO.task_category'].label).toBe('additive_reasoning')
    expect(replay.spec!.classifiers[0].criterion).not.toBe('edited')
    expect(replay.items.every(item => item.status === 'complete')).toBe(true)
    expect(replay.model).toBeUndefined()
    expect(replay.usage).toEqual({ input_tokens: 0, output_tokens: 0 })
    expect(replay.summary?.dataset?.label_provenance).toContain('No model calls are made')
  })
})
