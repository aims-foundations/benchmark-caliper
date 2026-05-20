# Benchmark Caliper Deployment

This website is deployed as one backend web service. The container builds the
Vite frontend and serves it from the FastAPI app, so Render only needs one
service for the MVP.

## Render

Use a **Web Service** backed by the root `Dockerfile`.

- Branch: `master`
- Root Directory: leave blank
- Runtime: Docker
- Instance type: Starter for MVP
- Instance count: 1
- Persistent disk: enabled
- Disk mount path: `/data`
- Disk size: 1 GB to start

Environment variables:

```bash
WEBSITE_BASE_PATH=/benchmark-caliper
WEBSITE_DATA_DIR=/data
WEBSITE_PUBLIC_URL=https://aimslab.stanford.edu/benchmark-caliper
WEBSITE_ALLOWED_ORIGINS=https://aimslab.stanford.edu,https://benchmark-caliper.onrender.com
```

Optional email variables:

```bash
RESEND_API_KEY=
RESEND_FROM=
FEEDBACK_TO=
```

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
