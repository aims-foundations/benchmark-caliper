import { useState } from 'react'

/* ============================================================
   SiteHeader — a faithful port of the AIMS site header.

   Benchmark Caliper is a separate app proxied into
   aimslab.stanford.edu, so it can't inherit the AIMS Next.js
   layout's <SiteHeader>. This re-implements that component
   (web/components/site-header.tsx in aims-foundations/aimslab)
   for our plain-React app: same markup, same styling, same
   dropdown + mobile-menu behaviour.

   Differences forced by being a separate app:
     - all hrefs are absolute (back to aimslab.stanford.edu)
     - active state is static — this app *is* Benchmark Caliper —
       instead of derived from a router pathname.
   Labels + hrefs mirror `primaryNavigation` in content/site.ts.
   ============================================================ */

const SITE = 'https://aimslab.stanford.edu'

type NavLeaf = { href: string; label: string; current?: boolean }
type NavGroup = { label: string; children: NavLeaf[] }
type NavItem = NavLeaf | NavGroup

const navItems: NavItem[] = [
  { href: `${SITE}/research`, label: 'Research' },
  { href: `${SITE}/textbook/`, label: 'Textbook' },
  { href: `${SITE}/competition`, label: 'Competition' },
  { href: `${SITE}/workshop`, label: 'Workshop' },
  {
    label: 'Software',
    children: [
      { href: `${SITE}/torch_measure`, label: 'torch_measure' },
      { href: `${SITE}/measurement-db`, label: 'measurement-db' },
      {
        href: `${SITE}/benchmark-caliper/`,
        label: 'Benchmark Caliper',
        current: true,
      },
    ],
  },
  { href: `${SITE}/cs321m`, label: 'Course' },
]

function isGroup(item: NavItem): item is NavGroup {
  return 'children' in item
}

function groupActive(group: NavGroup): boolean {
  return group.children.some((c) => c.current)
}

function Caret({ open }: { open: boolean }) {
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 16 16"
      width="12"
      height="12"
      fill="none"
      className={open ? 'site-caret is-open' : 'site-caret'}
    >
      <path
        d="M4 6l4 4 4-4"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function SiteHeader() {
  const [menuOpen, setMenuOpen] = useState(false)
  const [openGroup, setOpenGroup] = useState<string | null>(null)

  function closeMenu() {
    setMenuOpen(false)
  }

  /* ---- Desktop: a single leaf link ---- */
  function DesktopLeaf({ leaf }: { leaf: NavLeaf }) {
    return (
      <a
        className={
          leaf.current ? 'site-navlink is-active' : 'site-navlink'
        }
        href={leaf.href}
      >
        {leaf.label}
        {leaf.current && <span className="site-navunderline" />}
      </a>
    )
  }

  /* ---- Desktop: a dropdown group ---- */
  function DesktopGroup({ group }: { group: NavGroup }) {
    const open = openGroup === group.label
    const active = groupActive(group)
    return (
      <div
        className="site-navgroup"
        onMouseEnter={() => setOpenGroup(group.label)}
        onMouseLeave={() => setOpenGroup(null)}
        onFocus={() => setOpenGroup(group.label)}
        onBlur={(e) => {
          if (!e.currentTarget.contains(e.relatedTarget as Node)) {
            setOpenGroup(null)
          }
        }}
        onKeyDown={(e) => {
          if (e.key === 'Escape') setOpenGroup(null)
        }}
      >
        <button
          type="button"
          aria-haspopup="true"
          aria-expanded={open}
          onClick={() => setOpenGroup(open ? null : group.label)}
          className={
            'site-navlink site-navgroup-btn' +
            (active || open ? ' is-active' : '')
          }
        >
          {group.label}
          <Caret open={open} />
          {active && <span className="site-navunderline group" />}
        </button>

        {open && (
          <div className="site-navmenu">
            {group.children.map((child) => (
              <a
                key={child.href}
                className={
                  child.current
                    ? 'site-navmenu-item is-active'
                    : 'site-navmenu-item'
                }
                href={child.href}
                {...(child.current
                  ? { 'aria-current': 'page' as const }
                  : {})}
              >
                {child.label}
              </a>
            ))}
          </div>
        )}
      </div>
    )
  }

  /* ---- Mobile: a single leaf link ---- */
  function MobileLeaf({
    leaf,
    nested = false,
  }: {
    leaf: NavLeaf
    nested?: boolean
  }) {
    return (
      <a
        className={
          'site-mobilelink' +
          (nested ? ' nested' : '') +
          (leaf.current ? ' is-active' : '')
        }
        href={leaf.href}
        onClick={closeMenu}
      >
        {leaf.label}
      </a>
    )
  }

  return (
    <header className="site-header">
      <div className="site-header-shell">
        <div className="site-header-row">
          <a className="site-brand" href={SITE} onClick={closeMenu}>
            <span className="site-brand-mark">AIMS</span>
            <span className="site-brand-tick" aria-hidden="true" />
            <span className="site-brand-label">AI Measurement Science</span>
          </a>

          {/* Desktop nav */}
          <nav className="site-nav-desktop" aria-label="AIMS">
            {navItems.map((item) =>
              isGroup(item) ? (
                <DesktopGroup key={item.label} group={item} />
              ) : (
                <DesktopLeaf key={item.href} leaf={item} />
              ),
            )}
          </nav>

          {/* Mobile menu button */}
          <button
            type="button"
            className="site-menu-btn"
            onClick={() => setMenuOpen((open) => !open)}
            aria-expanded={menuOpen}
            aria-label="Toggle navigation menu"
          >
            {menuOpen ? 'Close' : 'Menu'}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="site-mobile-menu">
          <div className="site-header-shell">
            <nav className="site-mobile-nav">
              {navItems.map((item) =>
                isGroup(item) ? (
                  <div key={item.label} className="site-mobile-group">
                    <p className="site-mobile-grouplabel">{item.label}</p>
                    {item.children.map((child) => (
                      <MobileLeaf key={child.href} leaf={child} nested />
                    ))}
                  </div>
                ) : (
                  <MobileLeaf key={item.href} leaf={item} />
                ),
              )}
            </nav>
          </div>
        </div>
      )}
    </header>
  )
}
