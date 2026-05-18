import { useState, type FormEvent } from 'react'
import type { Question } from '../api'

interface Props {
  questions: Question[]
  onSubmit: (answers: Array<{ id: string; answer: string }>) => void
  onChangeKey: () => void
}

export function AnswerForm({ questions, onSubmit, onChangeKey }: Props) {
  const [answers, setAnswers] = useState<Record<string, string>>({})

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
        what your deployment actually requires. A short answer is fine — it's
        the structure that matters, not the length.
      </p>

      <ol className="question-list">
        {questions.map((q) => (
          <li key={q.id}>
            <label>
              <span className="question-header">
                <span className="dim-tag">{q.dimension}</span>
                <span className="question-text">{q.question}</span>
              </span>
              <textarea
                rows={3}
                maxLength={5000}
                value={answers[q.id] ?? ''}
                onChange={(e) => handleChange(q.id, e.target.value)}
                required
              />
            </label>
          </li>
        ))}
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
