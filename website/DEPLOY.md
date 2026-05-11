# Deploying the validity-analyzer website

This guide gets the website on a real public URL using **Fly.io**. Fly was picked for v0 because:

- Single command per service to deploy.
- Persistent volumes are first-class (we need one for SQLite + tier-3 blobs).
- EU regions exist (Frankfurt, Amsterdam, London, Madrid, Stockholm) — keeps the GDPR story simple if we host EU users.
- Free tier covers our v0 traffic; ~$5/mo covers the small persistent volume.

The same Dockerfiles work on Render, AWS App Runner, or any other Docker-friendly host. If you pick something else, the structure below should map.

> **Before deploying**: walk the [SECURITY.md](SECURITY.md) checklist end to end. Pre-launch items that are still open block a public URL — most importantly: domain, HTTPS cert, real `security@` email, pre-launch security review.

---

## One-time setup

Install the Fly CLI:

```bash
brew install flyctl       # macOS
# or
curl -L https://fly.io/install.sh | sh
```

Authenticate:

```bash
flyctl auth signup        # or `flyctl auth login` if you already have an account
```

---

## Deploy the backend

The backend image needs to see `anthropic_api_package/` at build time, so the **build context is the repo root**, not `website/server/`. We give Fly its own config file in the server directory but tell it where to look.

### 1. Create a `fly.backend.toml` at the repo root

```toml
app = "validity-backend"        # change to a unique app name
primary_region = "fra"          # Frankfurt; pick the one closest to your users

[build]
  dockerfile = "website/server/Dockerfile"

[mounts]
  source = "backend_data"
  destination = "/app/website/server/data"

[env]
  WEBSITE_ALLOWED_ORIGINS = "https://validity-frontend.fly.dev"  # update with your real frontend URL

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  [http_service.checks]
    [http_service.checks.healthz]
      method = "GET"
      path = "/healthz"
      interval = "30s"
      timeout = "5s"

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
```

### 2. Launch from the repo root

```bash
# from the repository root
flyctl launch --config fly.backend.toml --no-deploy
flyctl volumes create backend_data --region fra --size 1 --config fly.backend.toml
flyctl deploy --config fly.backend.toml
```

`flyctl launch` registers the app. The volume is needed for SQLite + tier-3 blobs to survive restarts.

### 3. Confirm

```bash
curl https://validity-backend.fly.dev/healthz
# {"status":"ok"}
```

---

## Deploy the frontend

The frontend image just serves the built React app and proxies `/api/*` to the backend.

### 1. Update `client/nginx.conf`

The `proxy_pass` in `nginx.conf` currently points at the docker-compose service name `backend`. For the deployed setup, change it to your backend's Fly URL:

```nginx
proxy_pass https://validity-backend.fly.dev;
```

(Or, if you use Fly's private networking, point it at `http://validity-backend.internal:8000` and add `flycast` configuration on the backend.)

### 2. `fly.frontend.toml`

```toml
app = "validity-frontend"
primary_region = "fra"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 80
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

### 3. Deploy

```bash
cd website/client
flyctl launch --config fly.frontend.toml --no-deploy
flyctl deploy --config fly.frontend.toml
```

### 4. Update the backend's `WEBSITE_ALLOWED_ORIGINS`

Set it to whatever Fly assigned to the frontend:

```bash
# from the repository root
flyctl secrets set WEBSITE_ALLOWED_ORIGINS="https://validity-frontend.fly.dev" --config fly.backend.toml
```

---

## Wire up retention

The 90-day cleanup needs to run once a day. Fly has built-in scheduled machines:

```bash
flyctl machine run \
  --schedule daily \
  --command "python3 -m website.server.retention" \
  --region fra \
  --config fly.backend.toml \
  validity-backend:latest
```

This runs `retention.py` once a day on a fresh machine that exits when done.

---

## Custom domain

```bash
# point your DNS A/AAAA records at Fly first, then:
flyctl certs create validity.example.org --config fly.frontend.toml
```

Fly auto-issues a Let's Encrypt cert.

After the domain is live, update:

- `WEBSITE_ALLOWED_ORIGINS` on the backend to the new origin.
- The privacy notice and `SECURITY.md` to reference the real domain.
- HSTS preload — only if you're confident, since it's hard to undo.

---

## Smoke test the deploy

After everything is up:

```bash
curl https://validity-frontend.example.org/healthz
# {"status":"ok"}

curl -I https://validity-frontend.example.org/
# Expect: 200, Strict-Transport-Security header, CSP header
```

Then click through the full flow with a real Anthropic key. A 20-page paper end-to-end should:

1. Show the consent gate
2. Take 3–10 minutes total to score
3. Cost roughly $1.50–$2.50 of Anthropic spend on the user's key (at Haiku 4.5 / Sonnet 4.6 / Opus 4.7 rates; web search adds $10/1k searches)
4. Leave NO Anthropic key bytes in our SQLite or blobs (verify by `flyctl ssh console` and `grep sk-ant-` over the `/app/website/server/data` directory)

---

## Tearing it down

```bash
flyctl apps destroy validity-frontend
flyctl apps destroy validity-backend
```

---

## What this guide does NOT do

- Set up CI for automatic deploys. Add later via GitHub Actions + `flyctl deploy --remote-only`.
- Configure observability (Sentry, structured-log shipping). Add when you actually want dashboards.
- Provision Postgres or Cloudflare R2. v0 stays on SQLite + local FS; migrate at v1+ when you have multi-machine deploy needs.
- Cover the security-review pass. That's [SECURITY.md](SECURITY.md), and it has to be done before pointing a public domain at this.
