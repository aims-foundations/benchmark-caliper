# Incident Response Runbook

What to do when something goes wrong with the validity-analyzer website. Five phases. Keep this document short enough that an on-call person can actually read it during an incident.

This satisfies SECURITY.md item 9.5. Reviewed on the same quarterly cadence as the rest of SECURITY.md.

> **Read this once before going on call.** When an incident hits, you'll re-skim it, not study it.

---

## Phase 1 — Discover

How an incident reaches us, in priority order:

1. **Uptime monitor alert** (configure on deploy — see DEPLOY.md). Pages the on-call.
2. **Sentry / error tracker** (configure on deploy). High-volume errors trip a threshold.
3. **`security@` email** (configure with the domain). A user or external researcher reports a vulnerability.
4. **A team member notices** during normal use. The most common channel until we have real monitoring.

Acknowledge the alert within 15 minutes during business hours, 1 hour after-hours. Even a "I see it, looking" reply in whatever channel the alert came through.

---

## Phase 2 — Triage

Decide severity within the first 30 minutes:

| Severity | Meaning | Examples |
|---|---|---|
| **SEV-1** | User API keys are at risk of leaking, or user data has actually leaked | Backend writes `sk-ant-...` to a log. Database file has been exfiltrated. PDF blobs are world-readable. |
| **SEV-2** | Non-credential user data is exposed, or the site is producing wrong results | Tier-3 blobs accessible without a valid run_id. Scoring step produces empty JSON. |
| **SEV-3** | Site is down or degraded but no data is at risk | Backend container crashing. Anthropic API outage taking us down. |
| **SEV-4** | Cosmetic / non-blocking bug | Footer link broken. Wrong color on a button. |

**The decision rule:** when in doubt, escalate up one level. A SEV-3 you treat as SEV-2 wastes an hour. A SEV-2 you treat as SEV-3 leaks data.

---

## Phase 3 — Contain

Specific commands for the most likely SEV-1 / SEV-2 scenarios:

### "We're writing API keys somewhere we shouldn't"

```bash
# 1. Pull the production server out of the load balancer (host-specific)
flyctl scale count 0 --config fly.backend.toml
# or whichever your provider's equivalent is.

# 2. Confirm scope. SSH into a stopped instance and grep:
flyctl ssh console --config fly.backend.toml
grep -rn "sk-ant-" /app/website/server/data 2>&1 | head -20
# Note every file and line that matched.

# 3. Snapshot the affected volume for forensics before any cleanup:
flyctl volumes snapshots create <volume-id>
```

If the leak is confirmed, **don't restart the service** until the root-cause code change is identified and patched. A restart with the same bug repeats the leak.

### "Someone got our SQLite or blob storage"

```bash
# 1. Same scale-down as above.
# 2. Rotate the application's own secrets (deploy token, DB password if
#    you migrated to Postgres, anything in the hosting provider's secret
#    manager). The user API keys are NOT in that list — they're in users'
#    browsers — so user-side rotation isn't ours to do, but we DO need to
#    notify users (Phase 4) so they can rotate them out of caution.
# 3. Preserve evidence: snapshot the volume, save access logs from the
#    edge for the relevant window.
```

### "Web search / Opus call is leaking user data via Anthropic"

This isn't really our incident to fix (Anthropic's pipeline), but it's our incident to communicate. Escalate to Anthropic via their support, then notify our users that their content reached Anthropic as the prompt always does, and the question is whether Anthropic's downstream handling matched their stated policy.

### "Site is down but data is safe (SEV-3)"

Restart, check logs, scale up if it's load. Don't touch users until you understand the cause.

---

## Phase 4 — Notify users

**Trigger threshold:** any SEV-1 or SEV-2 with confirmed user-data exposure.

**Timeline:** within 72 hours of confirmation. GDPR mandates this; we follow it regardless of jurisdiction.

**Channel:** email to affected users using the addresses they registered (we don't have those for v0 — when we add accounts in v1+, this gets concrete). For v0 with no accounts, post a notice at the top of the website until the next quarterly SECURITY.md review.

**Content** (keep it factual, not legal-ese):
1. What happened (one sentence)
2. What data was potentially exposed (specific: "deployment descriptions submitted between dates X and Y")
3. What we've done (containment + fix steps, concrete)
4. What the user should do (e.g., "rotate your Anthropic key", "use the delete-my-data endpoint")
5. How to contact us with questions

A draft template lives in `INCIDENT_NOTIFICATION_TEMPLATE.md` (write this once when you have a real domain — not yet).

---

## Phase 5 — Postmortem

Within one week of resolution:

1. **Write a postmortem document.** What happened, when, who detected, what was the impact, what was the root cause, what we did to contain, what we'll do to prevent recurrence.
2. **No blame, all systems.** The goal is finding the system change that prevents the next occurrence — not identifying a person to fault.
3. **Add new SECURITY.md items** if the incident reveals a gap in our checklist. The whole point of the checklist is to grow when reality finds holes in it.
4. **Share with the team.** Brief readout at the next meeting.

Postmortems live in `postmortems/YYYY-MM-DD-short-name.md`. (Directory doesn't exist yet; first incident creates it.)

---

## Contacts

To be filled in on deploy. Placeholders only:

| Role | Person | How to reach |
|---|---|---|
| On-call (rotating) | TBD | TBD |
| `security@` email | TBD | TBD |
| Anthropic provider escalation | n/a | <https://support.anthropic.com> |
| Hosting provider escalation | TBD (Fly / Render / etc) | TBD |
| Domain registrar | TBD | TBD |

---

## Drills

Once a quarter (paired with the SECURITY.md review), simulate a SEV-2 by walking through this runbook end-to-end. Even just talking through "if our SQLite file leaked, what would we actually do in the next 60 minutes" surfaces gaps faster than waiting for a real incident.