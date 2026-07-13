import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { App } from './App'

// Self-hosted AIMS fonts. Roboto Mono comes from @fontsource; Google Sans
// Flex (the AIMS redesign grotesk, not packaged on fontsource) is bundled
// from src/fonts via an @font-face in App.css. Vite serves both same-origin,
// so the strict CSP (default-src 'self') needs no change — no external font
// requests.
import '@fontsource/roboto-mono/latin-400.css'
import '@fontsource/roboto-mono/latin-500.css'
import '@fontsource/roboto-mono/latin-700.css'

// Order matters: the verbatim main-site stylesheet first, then App.css
// with the app's own styles and the supplements/overrides it needs.
import './aims-redesign.css'
import './App.css'

const rootEl = document.getElementById('root')
if (!rootEl) throw new Error('#root not found')

createRoot(rootEl).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
