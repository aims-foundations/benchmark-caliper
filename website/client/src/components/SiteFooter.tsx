/* ============================================================
   SiteFooter — a faithful port of the AIMS site footer.

   Ported from web/components/site-footer.tsx in
   aims-foundations/aimslab: the cardinal-red footer with the
   brand block, Pages / More link columns, and the bottom bar
   (copyright, Accessibility, GitHub + Discord).

   Differences forced by being a separate proxied app:
     - all hrefs are absolute (back to aimslab.stanford.edu)
     - the Phosphor icon components are inlined as SVGs
     - a "Privacy notice" link is added to the bottom bar; the
       privacy notice must be reachable from the footer per
       website/SECURITY.md.
   ============================================================ */

const SITE = 'https://aimslab.stanford.edu'
const GITHUB_URL = 'https://github.com/aims-foundations/aimslab'
const DISCORD_URL = 'https://discord.gg/UVseUQ983v'

const footerNav = [
  { href: `${SITE}/about`, label: 'About' },
  { href: `${SITE}/cs321m`, label: 'CS321M' },
  { href: `${SITE}/torch_measure`, label: 'Software' },
  { href: `${SITE}/competition`, label: 'Competition' },
]

const footerSecondary = [
  { href: `${SITE}/news`, label: 'News' },
  { href: `${SITE}/resources`, label: 'Resources' },
  { href: `${SITE}/textbook/`, label: 'Textbook' },
  { href: DISCORD_URL, label: 'Discord' },
]

// Phosphor Icons, "regular" weight — the exact icons the AIMS footer uses.
function GithubLogo() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 256 256"
      fill="currentColor"
      aria-hidden="true"
    >
      <path d="M208.31,75.68A59.78,59.78,0,0,0,202.93,28,8,8,0,0,0,196,24a59.75,59.75,0,0,0-48,24H124A59.75,59.75,0,0,0,76,24a8,8,0,0,0-6.93,4,59.78,59.78,0,0,0-5.38,47.68A58.14,58.14,0,0,0,56,104v8a56.06,56.06,0,0,0,48.44,55.47A39.8,39.8,0,0,0,96,192v8H72a24,24,0,0,1-24-24A40,40,0,0,0,8,136a8,8,0,0,0,0,16,24,24,0,0,1,24,24,40,40,0,0,0,40,40H96v16a8,8,0,0,0,16,0V192a24,24,0,0,1,48,0v40a8,8,0,0,0,16,0V192a39.8,39.8,0,0,0-8.44-24.53A56.06,56.06,0,0,0,216,112v-8A58.14,58.14,0,0,0,208.31,75.68ZM200,112a40,40,0,0,1-40,40H112a40,40,0,0,1-40-40v-8a41.74,41.74,0,0,1,6.9-22.48A8,8,0,0,0,80,73.83a43.81,43.81,0,0,1,.79-33.58,43.88,43.88,0,0,1,32.32,20.06A8,8,0,0,0,119.82,64h32.35a8,8,0,0,0,6.74-3.69,43.87,43.87,0,0,1,32.32-20.06A43.81,43.81,0,0,1,192,73.83a8.09,8.09,0,0,0,1,7.65A41.72,41.72,0,0,1,200,104Z" />
    </svg>
  )
}

function DiscordLogo() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 256 256"
      fill="currentColor"
      aria-hidden="true"
    >
      <path d="M104,140a12,12,0,1,1-12-12A12,12,0,0,1,104,140Zm60-12a12,12,0,1,0,12,12A12,12,0,0,0,164,128Zm74.45,64.9-67,29.71a16.17,16.17,0,0,1-21.71-9.1l-8.11-22q-6.72.45-13.63.46t-13.63-.46l-8.11,22a16.18,16.18,0,0,1-21.71,9.1l-67-29.71a15.93,15.93,0,0,1-9.06-18.51L38,58A16.07,16.07,0,0,1,51,46.14l36.06-5.93a16.22,16.22,0,0,1,18.26,11.88l3.26,12.84Q118.11,64,128,64t19.4.93l3.26-12.84a16.21,16.21,0,0,1,18.26-11.88L205,46.14A16.07,16.07,0,0,1,218,58l29.53,116.38A15.93,15.93,0,0,1,238.45,192.9ZM232,178.28,202.47,62s0,0-.08,0L166.33,56a.17.17,0,0,0-.17,0l-2.83,11.14c5,.94,10,2.06,14.83,3.42A8,8,0,0,1,176,86.31a8.09,8.09,0,0,1-2.16-.3A172.25,172.25,0,0,0,128,80a172.25,172.25,0,0,0-45.84,6,8,8,0,1,1-4.32-15.4c4.82-1.36,9.78-2.48,14.82-3.42L89.83,56s0,0-.12,0h0L53.61,61.93a.17.17,0,0,0-.09,0L24,178.33,91,208a.23.23,0,0,0,.22,0L98,189.72a173.2,173.2,0,0,1-20.14-4.32A8,8,0,0,1,82.16,170,171.85,171.85,0,0,0,128,176a171.85,171.85,0,0,0,45.84-6,8,8,0,0,1,4.32,15.41A173.2,173.2,0,0,1,158,189.72L164.75,208a.22.22,0,0,0,.21,0Z" />
    </svg>
  )
}

export function SiteFooter({
  onPrivacyClick,
}: {
  /** Opens the in-app privacy notice modal. */
  onPrivacyClick?: () => void
}) {
  return (
    <footer className="site-footer">
      <div className="site-footer-shell">
        <div className="site-footer-grid">
          <div className="site-footer-brandcol">
            <div className="site-footer-brand">
              <span className="site-footer-mark">AIMS</span>
              <span className="site-footer-tick" aria-hidden="true" />
              <span className="site-footer-brandlabel">
                AI Measurement Science
              </span>
            </div>
            <p className="site-footer-desc">
              A community for AI Measurement Science, bringing together
              research, teaching, and public-facing engagement around how AI
              systems are evaluated, understood, and improved.
            </p>
            <p className="site-footer-addr">Stanford, California 94305</p>
          </div>

          <div>
            <p className="site-footer-coltitle">Pages</p>
            <ul className="site-footer-list">
              {footerNav.map((item) => (
                <li key={item.href}>
                  <a className="site-footer-link" href={item.href}>
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <p className="site-footer-coltitle">More</p>
            <ul className="site-footer-list">
              {footerSecondary.map((item) => (
                <li key={item.href}>
                  <a className="site-footer-link" href={item.href}>
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="site-footer-bottom">
          <div className="site-footer-legal">
            <p>
              © {new Date().getFullYear()} AIMS — AI Measurement Science
            </p>
            <a
              href="https://uit.stanford.edu/accessibility"
              className="site-footer-legal-link"
            >
              Accessibility
            </a>
            {onPrivacyClick && (
              <button
                type="button"
                className="site-footer-legal-link site-footer-privacy"
                onClick={onPrivacyClick}
              >
                Privacy notice
              </button>
            )}
          </div>
          <div className="site-footer-social">
            <a
              href={GITHUB_URL}
              rel="noopener noreferrer"
              target="_blank"
              className="site-footer-icon"
              aria-label="AIMS on GitHub"
            >
              <GithubLogo />
            </a>
            <a
              href={DISCORD_URL}
              rel="noopener noreferrer"
              target="_blank"
              className="site-footer-icon"
              aria-label="AIMS Discord"
            >
              <DiscordLogo />
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}
