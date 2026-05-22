import { useEffect, useRef } from 'react'

/* ============================================================
   MatrixBackdrop — response-matrix watermark behind the header.

   Ported from the AIMS site's BinaryMatrixBackdrop. A grid of
   small rounded squares (correct = lagunita teal, incorrect =
   poppy coral, unobserved = empty). Two stacked layers render
   the same per-cell state:
     1. Base      — faint baseline, always visible
     2. Highlight — bright + scaled, masked by a radial spotlight
        that follows the cursor with a short fading trail.

   Pointer movement only updates CSS custom properties on the
   container; the cells themselves never re-render.
   ============================================================ */

// Matched to the AIMS home hero (binary-matrix-backdrop): 30 rows, gap 5px,
// 0.12 base opacity. COLS is 88 (not the AIMS 96) because our band is the
// viewport minus the 17rem sidebar — 88 keeps the cells the same ~12px size.
const ROWS = 30
const COLS = 88

const BASE_OPACITY = 0.12
const HIGHLIGHT_OPACITY = 0.95
const HIGHLIGHT_RADIUS_PX = 48
const HIGHLIGHT_CORE = 0.45 // share of radius at full opacity before fade
const HIGHLIGHT_SCALE = 1.4
const HIGHLIGHT_LIFT_PX = 1

// Trail: sample cursor position every TRAIL_INTERVAL_MS ms, keep the last
// TRAIL_LENGTH positions; older slots get lower alpha so the tail fades.
const TRAIL_LENGTH = 6
const TRAIL_INTERVAL_MS = 45
const TRAIL_ALPHAS = [1.0, 0.78, 0.6, 0.44, 0.3, 0.18]

const CORRECT_COLOR = 'color-mix(in srgb, var(--lagunita) 92%, white)'
const INCORRECT_COLOR = 'color-mix(in srgb, var(--poppy) 80%, white)'

type CellState = 'correct' | 'incorrect' | 'unobserved'

function hash(r: number, c: number, salt: number): number {
  const s = Math.sin(r * 12.9898 + c * 78.233 + salt * 37.719) * 43758.5453
  return s - Math.floor(s)
}

function buildCellStates(): CellState[] {
  const out: CellState[] = []
  for (let r = 0; r < ROWS; r++) {
    const ability = 0.45 + ((ROWS - 1 - r) / (ROWS - 1)) * 0.45
    for (let c = 0; c < COLS; c++) {
      // Observation gate: roughly half of cells are observed.
      if (hash(r, c, 1) > 0.55) {
        out.push('unobserved')
        continue
      }
      const difficulty = 0.3 + (c / (COLS - 1)) * 0.55
      const logit = (ability - difficulty) * 5
      const p = 1 / (1 + Math.exp(-logit))
      out.push(hash(r, c, 2) < p ? 'correct' : 'incorrect')
    }
  }
  return out
}

const CELL_STATES = buildCellStates()

function BackdropGrid({ variant }: { variant: 'base' | 'highlight' }) {
  const isHighlight = variant === 'highlight'
  return (
    <div
      className="matrix-grid"
      style={{ gridTemplateColumns: `repeat(${COLS}, minmax(0, 1fr))` }}
    >
      {CELL_STATES.map((state, i) => {
        if (state === 'unobserved')
          return <div key={i} className="matrix-cell-box" />
        const color = state === 'correct' ? CORRECT_COLOR : INCORRECT_COLOR
        return (
          <div
            key={i}
            className="matrix-cell-box"
            style={{
              backgroundColor: color,
              transform: isHighlight
                ? `translate3d(0, -${HIGHLIGHT_LIFT_PX}px, 0) scale(${HIGHLIGHT_SCALE})`
                : undefined,
            }}
          />
        )
      })}
    </div>
  )
}

export function MatrixBackdrop() {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const el = containerRef.current
    if (!el) return

    const history: { x: number; y: number }[] = Array.from(
      { length: TRAIL_LENGTH },
      () => ({ x: -9999, y: -9999 }),
    )
    let lastX = -9999
    let lastY = -9999

    const onMove = (e: PointerEvent) => {
      const rect = el.getBoundingClientRect()
      lastX = e.clientX - rect.left
      lastY = e.clientY - rect.top
    }

    const onLeave = () => {
      lastX = -9999
      lastY = -9999
    }

    const tick = window.setInterval(() => {
      history.pop()
      history.unshift({ x: lastX, y: lastY })
      for (let i = 0; i < TRAIL_LENGTH; i++) {
        el.style.setProperty(`--mx${i}`, `${history[i]!.x}px`)
        el.style.setProperty(`--my${i}`, `${history[i]!.y}px`)
      }
    }, TRAIL_INTERVAL_MS)

    window.addEventListener('pointermove', onMove, { passive: true })
    document.addEventListener('pointerleave', onLeave)

    return () => {
      window.removeEventListener('pointermove', onMove)
      document.removeEventListener('pointerleave', onLeave)
      window.clearInterval(tick)
    }
  }, [])

  // One radial gradient per past cursor position, composited additively so
  // overlapping samples brighten and older samples fade.
  const maskValue = TRAIL_ALPHAS.map(
    (alpha, i) =>
      `radial-gradient(circle ${HIGHLIGHT_RADIUS_PX}px at var(--mx${i}, -9999px) var(--my${i}, -9999px), rgba(0,0,0,${alpha}) 0%, rgba(0,0,0,${alpha}) ${HIGHLIGHT_CORE * 100}%, transparent 100%)`,
  ).join(', ')

  return (
    <div ref={containerRef} aria-hidden="true" className="matrix-backdrop">
      {/* Base layer — faint baseline, always visible */}
      <div className="matrix-layer" style={{ opacity: BASE_OPACITY }}>
        <BackdropGrid variant="base" />
      </div>

      {/* Highlight layer — bright + scaled, masked to a soft circle */}
      <div
        className="matrix-layer"
        style={{
          opacity: HIGHLIGHT_OPACITY,
          WebkitMaskImage: maskValue,
          maskImage: maskValue,
          WebkitMaskComposite: 'source-over',
          maskComposite: 'add',
          filter:
            'drop-shadow(0 2px 8px rgba(0, 0, 0, 0.20)) drop-shadow(0 0 6px color-mix(in srgb, var(--lagunita) 60%, transparent))',
          willChange: 'filter, mask-image',
        }}
      >
        <BackdropGrid variant="highlight" />
      </div>
    </div>
  )
}
