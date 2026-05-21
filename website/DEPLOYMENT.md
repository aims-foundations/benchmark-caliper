# Benchmark Caliper Deployment

This website is deployed as one backend web service. The container builds the
Vite frontend and serves it from the FastAPI app, so Render only needs one
service for the MVP.

## Render

The repo root ships a `render.yaml` Blueprint that captures the whole service
(Docker, persistent disk, health check, env vars). The easy path:

1. In Render: **New > Blueprint**, pick the `validity-global-south` repo.
2. Render reads `render.yaml` and proposes the `benchmark-caliper` web service.
3. Fill in the three email values it asks for (left blank in the Blueprint):
   `RESEND_API_KEY`, `RESEND_FROM`, `FEEDBACK_TO`. The app runs without them
   (email falls back to a dry-run), so they can be added later.
4. Apply. Render builds the `Dockerfile` and deploys.

The Blueprint already sets these, so you do **not** type them by hand:

- Branch `master`, Runtime Docker, Starter plan, 1 instance
- Persistent disk `data` mounted at `/data`, 1 GB
- Health check path `/healthz`
- Env vars:

```bash
WEBSITE_BASE_PATH=/benchmark-caliper
WEBSITE_DATA_DIR=/data
WEBSITE_PUBLIC_URL=https://aimslab.stanford.edu/benchmark-caliper
WEBSITE_ALLOWED_ORIGINS=https://aimslab.stanford.edu,https://benchmark-caliper.onrender.com
```

### Manual setup (if not using the Blueprint)

Create a **Web Service** backed by the root `Dockerfile` with the same
settings listed above, and set the same env vars (plus the optional email
ones). Be sure to set the **Health Check Path** to `/healthz`.

### Data disk permissions

The container starts as root, lets `entrypoint.sh` `chown` the runtime-mounted
`/data` disk, then drops to the unprivileged `appuser`. This is why the first
run can write `runs.db` to the persistent disk even though the app itself is
non-root — no manual permission step is needed.

If using Render's Python runtime instead of Docker, the service must still
build the frontend before starting FastAPI:

```bash
pip install -r website/server/requirements.txt -r anthropic_api_package_release/requirements.txt && cd website/client && npm ci && WEBSITE_BASE_PATH=/benchmark-caliper npm run build
```

Start command:

```bash
uvicorn website.server.app:app --host 0.0.0.0 --port $PORT
```

The Docker path is preferred because it pins the Node and Python build
environment in one place.

## AIMS Vercel Proxy

The main AIMS site should proxy `/benchmark-caliper/*` to the Render origin.
Set this environment variable on the AIMS Vercel project:

```bash
BENCHMARK_CALIPER_PROXY_ORIGIN=https://benchmark-caliper.onrender.com
```

After the AIMS site redeploys, verify:

```bash
curl -I https://aimslab.stanford.edu/benchmark-caliper/
curl https://aimslab.stanford.edu/benchmark-caliper/healthz
```

The browser URL should stay on `aimslab.stanford.edu`.
