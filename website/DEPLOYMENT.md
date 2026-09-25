# Benchmark Caliper Deployment

This website is deployed as one backend web service. The container builds the
Vite frontend and serves it from the FastAPI app, so Render only needs one
service for the MVP.

The same image now serves the workflow selector, `/caliper`, and `/items` under
the existing `/benchmark-caliper` proxy. Existing `/run/{run_id}` links keep
working. No second service or AIMS proxy change is required.

## Item-review configuration

The website's Python requirements include the shared OpenAI judge and dataset
loader. Keep **one instance and one Uvicorn worker** for the in-memory item-review
jobs. A restart clears in-flight jobs and their results; users can download JSON
before restarting the service. The CLI's disk-based resume is separate.

Set an optional `HF_TOKEN` secret in Render with read access to the gated
`aims-foundations/measurement-db` dataset. If it is absent, the access form asks
each user for an authorized Hugging Face read token. Do not put a maintainer's
OpenAI key on the service: the new endpoint requires the caller's key.

Only the three tables pinned in `website/server/item_review_inventory.json` are
available in the hosted demo. Their dataset files download on first use and use
the Hugging Face cache. No dataset content, provider keys, or local CLI run
artifacts are bundled into the image. Results and deployment descriptions stay
in process memory for one hour after a review ends; source dataset files may
remain cached. The existing Caliper database and retention behavior are unchanged.

After deploying, verify the chooser, both workflows, and the catalog:

```bash
curl -f https://aimslab.stanford.edu/benchmark-caliper/healthz
curl -f https://aimslab.stanford.edu/benchmark-caliper/api/item-review/catalog
```

Open `/benchmark-caliper/`, `/benchmark-caliper/caliper`, and
`/benchmark-caliper/items` in the browser. Run a small real assessment with your
own key to validate account/model access and judge quality; automated tests use
mocked OpenAI responses and do not establish scoring quality.

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
