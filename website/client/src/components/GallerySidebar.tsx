import type { GalleryEntry } from '../api'

export interface SessionEntry {
  benchmarkName: string
  slug: string
}

interface Props {
  entries: GalleryEntry[]
  sessionEntry: SessionEntry | null
  /** id of the currently-viewed entry, or 'session', or null. */
  activeId: string | null
  /** False while the user's own pipeline is running — navigation locked. */
  enabled: boolean
  onSelectCurated: (id: string) => void
  onSelectSession: () => void
  onAddBenchmark: () => void
}

/**
 * Persistent left-hand gallery. Lists the curated expert assessments,
 * plus (if the user has finished their own run this session) a
 * "Your benchmark" entry, and an "Add your benchmark" button.
 *
 * The gallery is read-only navigation: while a pipeline run is in
 * progress (`enabled === false`) the entries are disabled so the user
 * cannot navigate away from their own run mid-flight.
 */
export function GallerySidebar({
  entries,
  sessionEntry,
  activeId,
  enabled,
  onSelectCurated,
  onSelectSession,
  onAddBenchmark,
}: Props) {
  return (
    <aside className="gallery-sidebar" aria-label="Benchmark gallery">
      <h2 className="gallery-title">Evaluated benchmarks</h2>
      <p className="gallery-hint">
        Reports from benchmarks our experts have already assessed. Click
        one to view its validity scores.
      </p>

      <ul className="gallery-list">
        {entries.map((e) => {
          const selected = activeId === e.id
          return (
            <li key={e.id}>
              <button
                type="button"
                className={
                  selected ? 'gallery-item selected' : 'gallery-item'
                }
                disabled={!enabled}
                aria-current={selected ? 'true' : undefined}
                onClick={() => onSelectCurated(e.id)}
              >
                <span className="gallery-item-name">{e.benchmarkName}</span>
                <span className="gallery-item-context">
                  {e.deploymentDescription || e.slug}
                </span>
              </button>
            </li>
          )
        })}
      </ul>

      {/* Pinned below the scrollable list — always visible. */}
      {sessionEntry && (
        <div className="gallery-session-pinned">
          <button
            type="button"
            className={
              activeId === 'session'
                ? 'gallery-item session selected'
                : 'gallery-item session'
            }
            disabled={!enabled}
            aria-current={activeId === 'session' ? 'true' : undefined}
            onClick={onSelectSession}
          >
            <span className="gallery-item-name">Your benchmark</span>
            <span className="gallery-item-context">
              {sessionEntry.benchmarkName || sessionEntry.slug}
            </span>
          </button>
        </div>
      )}

      <button
        type="button"
        className="gallery-add"
        disabled={!enabled}
        onClick={onAddBenchmark}
      >
        + Add your benchmark
      </button>
    </aside>
  )
}
