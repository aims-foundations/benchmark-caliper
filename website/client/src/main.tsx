import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { App } from './App'

// Self-hosted AIMS fonts (Source Sans 3 / Source Serif 4 / Roboto Mono).
// Vite bundles the woff2 files and serves them same-origin, so the strict
// CSP (default-src 'self') needs no change — no external font requests.
import '@fontsource/source-sans-3/latin-400.css'
import '@fontsource/source-sans-3/latin-500.css'
import '@fontsource/source-sans-3/latin-600.css'
import '@fontsource/source-sans-3/latin-700.css'
import '@fontsource/source-serif-4/latin-400.css'
import '@fontsource/roboto-mono/latin-400.css'
import '@fontsource/roboto-mono/latin-500.css'
import '@fontsource/roboto-mono/latin-700.css'

import './App.css'

const rootEl = document.getElementById('root')
if (!rootEl) throw new Error('#root not found')

createRoot(rootEl).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
