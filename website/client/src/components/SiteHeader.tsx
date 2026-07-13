import { useEffect, useState } from 'react'

/* ============================================================
   SiteHeader — a port of the AIMS redesigned header (RdHeader).

   Benchmark Caliper is a separate app proxied into
   aimslab.stanford.edu, so it can't inherit the AIMS Next.js
   layout's <RdHeader>. This re-implements that component
   (web/components/redesign/rd-header.tsx in
   aims-foundations/aimslab) for our plain-React app: same
   logo, same pill nav links, same hover-dropdown pill bar,
   same mobile menu.

   Nav sync: the main site publishes its `primaryNavigation`
   (single source of truth in web/content/site.ts) as a JSON
   manifest at /nav.json precisely so proxied sub-sites can
   stay in sync. In production this app is served under
   aimslab.stanford.edu/benchmark-caliper/, so a root-relative
   fetch of /nav.json is same-origin (CSP `connect-src 'self'`
   allows it) and always reflects the live nav — edit the nav
   on the main site and this header follows on next load.
   NAV_FALLBACK below is only the first paint + the safety net
   for local dev / direct-origin access, not something that
   needs manual updates on every nav change.
   ============================================================ */

const SITE = 'https://aimslab.stanford.edu'

type NavLeaf = { href: string; label: string; proxied?: boolean }
type NavGroup = { label: string; children: NavLeaf[] }
type NavItem = NavLeaf | NavGroup

/** Snapshot of the main site's primaryNavigation, used until /nav.json
    loads (and when it is unreachable: vite dev, tests, direct Render origin). */
const NAV_FALLBACK: NavItem[] = [
  { href: '/research', label: 'Research' },
  {
    label: 'Software & Data',
    children: [
      { href: '/software', label: 'Overview' },
      { href: '/torch_measure', label: 'torch_measure' },
      { href: '/measurement-db', label: 'Measurement Data Bank' },
      { href: '/benchmark-caliper/', label: 'Benchmark Caliper' },
    ],
  },
  { href: '/competition', label: 'Competition' },
  { href: '/workshop', label: 'Workshop' },
  {
    label: 'Education',
    children: [
      { href: `${SITE}/textbook/`, label: 'Textbook' },
      { href: '/cs321m', label: 'Course' },
    ],
  },
  { href: '/news', label: 'News' },
]

function isLeaf(value: unknown): value is NavLeaf {
  if (typeof value !== 'object' || value === null) return false
  const leaf = value as Record<string, unknown>
  return typeof leaf.href === 'string' && typeof leaf.label === 'string'
}

/** Validate the fetched manifest so a malformed payload can never break
    the header — anything unexpected falls back to the snapshot. */
function parseNav(data: unknown): NavItem[] | null {
  if (!Array.isArray(data) || data.length === 0) return null
  const items: NavItem[] = []
  for (const entry of data) {
    if (isLeaf(entry)) {
      items.push(entry)
      continue
    }
    if (
      typeof entry === 'object' &&
      entry !== null &&
      typeof (entry as Record<string, unknown>).label === 'string' &&
      Array.isArray((entry as Record<string, unknown>).children) &&
      ((entry as Record<string, unknown>).children as unknown[]).every(isLeaf)
    ) {
      const group = entry as { label: string; children: NavLeaf[] }
      items.push({ label: group.label, children: group.children })
      continue
    }
    return null
  }
  return items
}

/** Root-relative hrefs in the manifest are main-site routes; resolve them
    against the main site so links also work from a non-proxied origin. */
function absolute(href: string): string {
  try {
    return new URL(href, SITE).toString()
  } catch {
    return href
  }
}

/** This app *is* Benchmark Caliper — its entry is the current page. */
function isCurrent(href: string): boolean {
  try {
    const path = new URL(href, SITE).pathname.replace(/\/+$/, '')
    return path === '/benchmark-caliper'
  } catch {
    return false
  }
}

function useSyncedNav(): NavItem[] {
  const [nav, setNav] = useState<NavItem[]>(NAV_FALLBACK)

  useEffect(() => {
    // Dev/test builds have no main site to fetch from (and the app tests
    // mock global fetch); they render the snapshot.
    if (!import.meta.env.PROD) return
    const controller = new AbortController()
    fetch('/nav.json', { signal: controller.signal })
      .then(async (res) => {
        if (!res.ok) return
        const parsed = parseNav(await res.json())
        if (parsed) setNav(parsed)
      })
      .catch(() => {
        /* unreachable or invalid manifest — keep the snapshot */
      })
    return () => controller.abort()
  }, [])

  return nav
}

function isGroup(item: NavItem): item is NavGroup {
  return 'children' in item
}

/* AIMS logomark in the Stanford HAI style — ported from
   web/components/redesign/rd-logo.tsx. Inherits currentColor. */
function AimsMark({ height }: { height: number }) {
  const width = (height / 70) * 177
  return (
    <svg
      viewBox="0 0 177 70"
      width={width}
      height={height}
      fill="none"
      stroke="currentColor"
      strokeWidth="2.4"
      aria-hidden="true"
    >
      {/* A — nested chevrons + crossbar */}
      <path d="M 0 70 L 20 1 L 40 70" />
      <path d="M 4.7 70 L 20 17.2 L 35.3 70" />
      <path d="M 9.4 70 L 20 33.4 L 30.6 70" />
      <path d="M 14.2 53.5 H 25.8" />
      <path d="M 12.9 58 H 27.1" />

      {/* I — three verticals */}
      <path d="M 53 1 V 70" />
      <path d="M 57.5 1 V 70" />
      <path d="M 62 1 V 70" />

      {/* M — triple stems + nested center V */}
      <path d="M 75 1 V 70" />
      <path d="M 79.5 1 V 70" />
      <path d="M 84 1 V 70" />
      <path d="M 110 1 V 70" />
      <path d="M 114.5 1 V 70" />
      <path d="M 119 1 V 70" />
      <path d="M 75 1 L 97 48 L 119 1" />
      <path d="M 79.5 1 L 97 41 L 114.5 1" />
      <path d="M 84 1 L 97 34 L 110 1" />

      {/* S — two loops of concentric arcs */}
      <g transform="translate(132 0)">
        <path d="M 38.5 17 A 16 16 0 1 0 22.5 33 A 13.5 13.5 0 1 1 9 46.5" />
        <path d="M 34 17 A 11.5 11.5 0 1 0 22.5 28.5 A 18 18 0 1 1 4.5 46.5" />
        <path d="M 29.5 17 A 7 7 0 1 0 22.5 24 A 22.5 22.5 0 1 1 0 46.5" />
      </g>
    </svg>
  )
}

export function RdLogo({ height = 34 }: { height?: number }) {
  const textSize = height * 0.34
  return (
    <span className="inline-flex items-center" style={{ gap: height * 0.32 }}>
      <AimsMark height={height} />
      <span
        className="flex flex-col justify-center"
        style={{ fontSize: textSize, lineHeight: 1.3 }}
      >
        <span className="font-semibold">Stanford University</span>
        <span className="font-normal">AI Measurement Science</span>
      </span>
      <span className="sr-only">AIMS — AI Measurement Science</span>
    </span>
  )
}

function RdCaret() {
  return (
    <svg
      className="rd-nav-caret"
      width="11"
      height="7"
      viewBox="0 0 11 7"
      fill="none"
      aria-hidden="true"
    >
      <path
        d="M1 1.5 5.5 6l4.5-4.5"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function SiteHeader() {
  const navItems = useSyncedNav()
  const [mobileOpen, setMobileOpen] = useState(false)
  const [hidden, setHidden] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  // Same scroll choreography as RdHeader: transparent over the hero at the
  // top, warm + hairline once scrolled, slides away while scrolling down.
  useEffect(() => {
    let lastY = window.scrollY
    const onScroll = () => {
      const y = window.scrollY
      setScrolled(y > 24)
      setHidden(y > 120 && y > lastY)
      lastY = y
    }
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  // Markup below is verbatim from the main site's rd-header.tsx, with
  // three app-forced differences: next/link → <a>, hrefs resolved via
  // absolute(), and aria-current marking on the Benchmark Caliper entry.
  return (
    <header
      className={`rd-header ${scrolled || mobileOpen ? 'rd-header--scrolled' : ''} ${
        hidden && !mobileOpen ? 'rd-header--hidden' : ''
      }`}
    >
      <div className="rd-container flex items-center justify-between py-4">
        <a
          href={SITE}
          className="rd-wordmark"
          onClick={() => setMobileOpen(false)}
        >
          <RdLogo height={40} />
        </a>

        <nav className="hidden items-center gap-2 lg:flex" aria-label="AIMS">
          {navItems.map((item) =>
            isGroup(item) ? (
              <div key={item.label} className="rd-nav-item">
                <button type="button" className="rd-nav-link">
                  {item.label}
                  <RdCaret />
                </button>
                <div className="rd-dropdown">
                  {item.children.map((child) => (
                    <a
                      key={child.label}
                      href={absolute(child.href)}
                      {...(isCurrent(child.href)
                        ? {
                            'aria-current': 'page' as const,
                            className: 'is-current',
                          }
                        : {})}
                    >
                      {child.label}
                    </a>
                  ))}
                </div>
              </div>
            ) : (
              <a
                key={item.label}
                href={absolute(item.href)}
                className="rd-nav-link"
              >
                {item.label}
              </a>
            ),
          )}
        </nav>

        <button
          type="button"
          className="rd-mono lg:hidden"
          aria-expanded={mobileOpen}
          onClick={() => setMobileOpen((open) => !open)}
        >
          {mobileOpen ? 'Close' : 'Menu'}
        </button>
      </div>

      {mobileOpen && (
        <nav
          className="rd-container border-t border-black/10 pb-6 pt-2 lg:hidden"
          aria-label="AIMS"
        >
          {navItems.map((item) =>
            isGroup(item) ? (
              <div key={item.label} className="py-2">
                <div className="rd-mono pb-1 opacity-60">{item.label}</div>
                {item.children.map((child) => (
                  <a
                    key={child.label}
                    href={absolute(child.href)}
                    className="block py-1.5 pl-4 text-lg font-light"
                    onClick={() => setMobileOpen(false)}
                    {...(isCurrent(child.href)
                      ? { 'aria-current': 'page' as const }
                      : {})}
                  >
                    {child.label}
                  </a>
                ))}
              </div>
            ) : (
              <a
                key={item.label}
                href={absolute(item.href)}
                className="block py-2 text-lg font-light"
                onClick={() => setMobileOpen(false)}
              >
                {item.label}
              </a>
            ),
          )}
        </nav>
      )}
    </header>
  )
}
