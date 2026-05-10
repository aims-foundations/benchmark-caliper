import type { Question } from '../api'

interface Props {
  questions: Question[]
  runId: string
  slug: string
  onStartOver: () => void
  onChangeKey: () => void
}

export function QuestionsView({
  questions,
  runId,
  slug,
  onStartOver,
  onChangeKey,
}: Props) {
  return (
    <section className="questions">
      <h2>Elicitation questions</h2>
      <p className="help">
        These questions help close the gap between what the benchmark documents
        and what your deployment actually requires. The next slice will let you
        answer them; for now this is a preview of what Step 2 produced.
      </p>

      <ol className="question-list">
        {questions.map((q) => (
          <li key={q.id}>
            <span className="dim-tag">{q.dimension}</span>
            <span className="question-text">{q.question}</span>
          </li>
        ))}
      </ol>

      <dl className="run-meta">
        <dt>Slug</dt>
        <dd>
          <code>{slug}</code>
        </dd>
        <dt>Run ID</dt>
        <dd>
          <code>{runId}</code>
        </dd>
      </dl>

      <div className="actions">
        <button type="button" className="link" onClick={onChangeKey}>
          Change key
        </button>
        <button type="button" onClick={onStartOver}>
          Run another
        </button>
      </div>
    </section>
  )
}