import { RdLogo } from './SiteHeader'

/* ============================================================
   SiteFooter — a port of the AIMS redesigned footer (RdFooter).

   Ported from web/components/redesign/rd-footer.tsx in
   aims-foundations/aimslab: a dark-red band with the AIMS logo,
   address, and Get Involved / Stay in Touch columns, then a
   near-black band with Stanford + legal links.

   Differences forced by being a separate proxied app:
     - all hrefs are absolute (back to aimslab.stanford.edu)
     - a "Privacy notice" link is added to the legal row; the
       privacy notice must be reachable from the footer per
       website/SECURITY.md.
   ============================================================ */

const SITE = 'https://aimslab.stanford.edu'
const GITHUB_URL = 'https://github.com/aims-foundations/aimslab'
const DISCORD_URL = 'https://discord.gg/UVseUQ983v'

const getInvolved = [
  { href: `${SITE}/cs321m`, label: 'CS321M Course' },
  { href: `${SITE}/textbook/`, label: 'Textbook' },
  { href: `${SITE}/competition`, label: 'Competition' },
  { href: `${SITE}/workshop`, label: 'Workshop' },
  { href: `${SITE}/newsletter`, label: 'Newsletter' },
]

const stayInTouch = [
  { href: DISCORD_URL, label: 'Discord' },
  { href: GITHUB_URL, label: 'GitHub' },
  { href: `${SITE}/news/feed.xml`, label: 'Atom feed' },
]

const stanfordLinks = [
  { href: 'https://www.stanford.edu', label: 'Stanford Home' },
  { href: 'https://visit.stanford.edu/plan/', label: 'Maps & Directions' },
  { href: 'https://www.stanford.edu/search/', label: 'Search Stanford' },
  { href: 'https://emergency.stanford.edu', label: 'Emergency Info' },
]

const legalLinks = [
  { href: 'https://www.stanford.edu/site/terms/', label: 'Terms of Use' },
  { href: 'https://www.stanford.edu/site/privacy/', label: 'Privacy' },
  {
    href: 'https://uit.stanford.edu/security/copyright-infringement',
    label: 'Copyright',
  },
  {
    href: 'https://adminguide.stanford.edu/chapters/guiding-policies/1-5-4-ownership-and-use-stanford-trademarks-and-images',
    label: 'Trademarks',
  },
  {
    href: 'https://www.stanford.edu/site/accessibility/',
    label: 'Accessibility',
  },
]

export function SiteFooter({
  onPrivacyClick,
}: {
  /** Opens the in-app privacy notice modal. */
  onPrivacyClick?: () => void
}) {
  return (
    <footer className="rd-footer">
      <div className="rd-darkred-band">
        <div className="rd-container rd-footer-grid">
          <div className="rd-footer-brandcol">
            <RdLogo height={48} />
            <p className="rd-footer-addr">
              Stanford University
              <br />
              353 Jane Stanford Way
              <br />
              Stanford, CA 94305
            </p>
          </div>

          <div className="rd-footer-col">
            <div className="rd-mono rd-footer-coltitle">Get Involved</div>
            <ul className="rd-footer-list">
              {getInvolved.map((link) => (
                <li key={link.label}>
                  <a href={link.href} className="rd-footer-link">
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div className="rd-footer-col">
            <div className="rd-mono rd-footer-coltitle">Stay in Touch</div>
            <ul className="rd-footer-list">
              {stayInTouch.map((link) => (
                <li key={link.label}>
                  <a
                    href={link.href}
                    className="rd-footer-link"
                    rel="noopener noreferrer"
                    target="_blank"
                  >
                    {link.label}
                  </a>
                </li>
              ))}
            </ul>
            <p className="rd-footer-note">
              The newsletter carries short updates on course activity,
              resources, and software milestones.{' '}
              <a href={`${SITE}/newsletter`} className="rd-footer-underline">
                Subscribe
              </a>
            </p>
          </div>
        </div>
      </div>

      <div className="rd-dark-band">
        <div className="rd-container rd-footer-bottom">
          <ul className="rd-footer-inline">
            {stanfordLinks.map((link) => (
              <li key={link.label}>
                <a href={link.href} className="rd-footer-link">
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
          <ul className="rd-footer-inline dim">
            {legalLinks.map((link) => (
              <li key={link.label}>
                <a href={link.href} className="rd-footer-link">
                  {link.label}
                </a>
              </li>
            ))}
            {onPrivacyClick && (
              <li>
                <button
                  type="button"
                  className="rd-footer-link rd-footer-privacy"
                  onClick={onPrivacyClick}
                >
                  Privacy notice (this app)
                </button>
              </li>
            )}
          </ul>
          <p className="rd-footer-copy">
            © Stanford University. Stanford, California 94305.
          </p>
        </div>
      </div>
    </footer>
  )
}
