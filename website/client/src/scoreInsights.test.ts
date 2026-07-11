import { describe, it, expect } from 'vitest'
import { calibrateConfidence, parsePriorityWeights } from './scoreInsights'

describe('calibrateConfidence', () => {
  it('keeps high when at least two evidence streams are present', () => {
    const r = calibrateConfidence({
      confidence: 'high',
      evidence_quotes: ['[Q1] ...'],
      evidence_dataset: ['D1: ...'],
    })
    expect(r.streamCount).toBe(2)
    expect(r.calibrated).toBe('high')
    expect(r.downgraded).toBe(false)
  })

  it('downgrades high to medium with a single stream (the Output Form case)', () => {
    const r = calibrateConfidence({
      confidence: 'high',
      evidence_quotes: ['[Q1] a', '[Q2] b', '[Q3] c', '[Q4] d'],
      evidence_web_sources: [],
      evidence_dataset: [],
    })
    expect(r.streamCount).toBe(1)
    expect(r.reported).toBe('high')
    expect(r.calibrated).toBe('medium')
    expect(r.downgraded).toBe(true)
  })

  it('downgrades high to low when no stream carries evidence', () => {
    const r = calibrateConfidence({ confidence: 'high' })
    expect(r.streamCount).toBe(0)
    expect(r.calibrated).toBe('low')
    expect(r.downgraded).toBe(true)
  })

  it('never raises a cautious model up', () => {
    const r = calibrateConfidence({
      confidence: 'low',
      evidence_quotes: ['a'],
      evidence_web_sources: ['b'],
      evidence_dataset: ['c'],
    })
    expect(r.streamCount).toBe(3)
    expect(r.calibrated).toBe('low')
    expect(r.downgraded).toBe(false)
  })

  it('treats evidence_region_sources as a web stream (legacy fixtures)', () => {
    const r = calibrateConfidence({
      confidence: 'high',
      evidence_quotes: ['a'],
      evidence_region_sources: ['b'],
    })
    expect(r.streamCount).toBe(2)
    expect(r.calibrated).toBe('high')
  })

  it('derives a label even when the model omitted confidence', () => {
    const r = calibrateConfidence({ evidence_quotes: ['a'] })
    expect(r.reported).toBe(null)
    expect(r.calibrated).toBe('medium')
    expect(r.downgraded).toBe(false)
  })
})

describe('parsePriorityWeights', () => {
  const summary = [
    '## Dimension Priority Weights',
    '| Dimension | Priority | Rationale |',
    '|-----------|----------|-----------|',
    '| IO | LOWER | text |',
    '| IC | HIGH | text |',
    '| OO | MODERATE | text |',
  ].join('\n')

  it('parses the markdown table into a keyed map', () => {
    const p = parsePriorityWeights(summary)
    expect(p.input_ontology).toBe('LOWER')
    expect(p.input_content).toBe('HIGH')
    expect(p.output_ontology).toBe('MODERATE')
  })

  it('normalizes MEDIUM/LOW synonyms', () => {
    const p = parsePriorityWeights('| IF | MEDIUM | x |\n| OF | LOW | y |')
    expect(p.input_form).toBe('MODERATE')
    expect(p.output_form).toBe('LOWER')
  })

  it('returns an empty map for missing or unparseable input', () => {
    expect(parsePriorityWeights(undefined)).toEqual({})
    expect(parsePriorityWeights('no table here')).toEqual({})
  })
})
