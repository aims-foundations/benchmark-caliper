import { useState, type FormEvent } from 'react'
import type { Question } from '../api'

interface Props {
  questions: Question[]
  onSubmit: (answers: Array<{ id: string; answer: string }>) => void
  onChangeKey: () => void
  /** Optional pre-fill (used by demo mode to show expert answers). */
  initialAnswers?: Record<string, string>
}

// Mirrors the 6 validity dimensions in framework.yaml. The 2-letter codes
// (IO/IC/IF/OO/OC/OF) come from the model; we expand them here for the UI.
const DIMENSION_INFO: Record<string, { name: string; blurb: string }> = {
  IO: {
    name: 'Input Ontology',
    blurb:
      "Do the benchmark's input categories match the kinds of inputs your deployment will actually see?",
  },
  IC: {
    name: 'Input Content',
    blurb:
      'Are the actual examples — language, scenarios, cultural references — representative of your deployment context?',
  },
  IF: {
    name: 'Input Form',
    blurb:
      'Does the format and modality of inputs (length, structure, dialogue turns) match what your system will receive?',
  },
  OO: {
    name: 'Output Ontology',
    blurb:
      "Do the benchmark's output categories (labels, scoring axes) cover what your deployment actually cares about?",
  },
  OC: {
    name: 'Output Content',
    blurb:
      'Are the ground-truth answers what your users would consider correct in their context?',
  },
  OF: {
    name: 'Output Form',
    blurb:
      'Does the expected output format (length, structure, register) match what your deployment needs to produce?',
  },
}

export function AnswerForm({
  questions,
  onSubmit,
  onChangeKey,
  initialAnswers,
}: Props) {
  const [answers, setAnswers] = useState<Record<string, string>>(
    () => initialAnswers ?? {},
  )

  function handleChange(id: string, value: string): void {
    setAnswers((prev) => ({ ...prev, [id]: value }))
  }

  const allAnswered = questions.every(
    (q) => (answers[q.id] ?? '').trim().length > 0,
  )

  function handleSubmit(e: FormEvent<HTMLFormElement>): void {
    e.preventDefault()
    if (!allAnswered) return
    onSubmit(
      questions.map((q) => ({
        id: q.id,
        answer: (answers[q.id] ?? '').trim(),
      })),
    )
  }

  return (
    <form onSubmit={handleSubmit} className="answer-form">
      <h2>Answer the elicitation questions</h2>
      <p className="help">
        These questions close the gap between what the benchmark documents and
        what your deployment actually requires.
      </p>

      <ol className="question-list">
        {questions.map((q) => {
          const info = DIMENSION_INFO[q.dimension]
          return (
            <li key={q.id}>
              <label>
                <span className="question-header">
                  <span className="dim-tag">{q.dimension}</span>
                  <span className="dim-name-full">
                    {info?.name ?? q.dimension}
                  </span>
                </span>
                {info && <p className="dim-blurb">{info.blurb}</p>}
                <span className="question-text">{q.question}</span>
                <textarea
                  rows={3}
                  maxLength={5000}
                  value={answers[q.id] ?? ''}
                  onChange={(e) => handleChange(q.id, e.target.value)}
                  required
                />
              </label>
            </li>
          )
        })}
      </ol>

      <div className="actions">
        <button type="button" className="link" onClick={onChangeKey}>
          Change key
        </button>
        <button type="submit" disabled={!allAnswered}>
          Submit answers
        </button>
      </div>
    </form>
  )
}
