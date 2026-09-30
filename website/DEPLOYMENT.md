# Benchmark Caliper Deployment

This website is deployed as one backend web service. The container builds the
Vite frontend and serves it from the FastAPI app, so Render only needs one
service for the MVP.

The same image now serves the workflow selector, `/caliper`, `/items`, and `/item-analysis` under
the existing `/benchmark-caliper` proxy. Existing `/run/{run_id}` links keep
working. No second service or AIMS proxy change is required.

## Item-analysis configuration

The `/item-analysis` demo defaults to the real 14,015-item MMLU snapshot at
`aims-foundations/measurement-db-pp`, revision
`cc796d3545a6bd2e78b5513c13e60a6913d01e3f`, table `mmlu/items.parquet`.
Grant the server's `HF_TOKEN` read access to that repository. Its access can
differ from the `measurement-db` repository used by the separate `/items` flow.
The application downloads and verifies the table when preparing the first run;
no manual dataset transfer is needed. The source is cached privately at
`/data/item-analysis-sources/`. The original assessment and supplied classifier
specification ship with the code; dataset rows stay out of Git and image layers.

Visitors supply an OpenAI key for both specification generation and item
classification. Both steps use `gpt-6-luna` with low reasoning effort; the
server needs no OpenAI key of its own for this workflow.
Loading the supplied MMLU criteria requires no visitor key, but does require
server dataset access. An optional ten-item teaching example remains available
and is explicitly illustrative. Access errors are shown without silently
substituting teaching data.

`ITEM_ANALYSIS_PREPARED_DIR` remains an optional override for a manually prepared
snapshot. Leave it unset for direct Hugging Face loading. Local `results/`
directories remain excluded from Docker.

Use one instance and one worker. Each browser run copies the source inputs into
a private directory. Jobs expire one hour after a phase ends and cannot resume
after a server restart. The live catalog shows which examples are configured:

```bash
curl -f https://aimslab.stanford.edu/benchmark-caliper/api/item-analysis/catalog
```

Verify `/benchmark-caliper/item-analysis`, load MMLU's supplied criteria, and
confirm that all 14,015 items are available with unclassified items marked pending. This checks
the deployed pipeline without paid calls. Generation and classification require
a separate live test with a visitor's key.

## Item-review configuration

The website's Python requirements include the shared OpenAI judge and dataset
loader. Keep **one instance and one Uvicorn worker** for the item-review jobs.
Jobs and keys live in memory; results use private temporary SQLite files.
A restart clears in-flight jobs and their results; users can download JSON
before restarting the service. The CLI's disk-based resume is separate.

Set the server's `HF_TOKEN` secret in Render with read access to the gated
`aims-foundations/measurement-db` dataset. This is required for hosted item
reviews; visitors supply only their OpenAI API key. Missing server dataset
credentials disable new reviews and show a message to contact the maintainer.
Do not put a maintainer's OpenAI key on the service.

Each review assesses up to four items concurrently. Optionally set
`ITEM_REVIEW_CONCURRENCY` to an integer from 1 to 16 (default 4). With the existing
three-review limit, the default allows at most 12 simultaneous item requests
across the service. Lower the limit for constrained provider quotas; 1 restores
sequential assessment. Provider retries stay bounded by the same worker pool.
Concurrency does not change the sample or number of intended assessments, and
does not accelerate initial sample preparation. Stopping a run cancels every
worker; requests already sent may still be billed.

The Blueprint declares `HF_TOKEN` with `sync: false`, so its value stays out of
Git. For an existing service, add the secret under **Environment** in Render;
updating the Blueprint alone does not populate a new `sync: false` variable.
See [Render's secret configuration](https://render.com/docs/blueprint-spec#prompting-for-secret-values).
The local machine's saved Hugging Face login is not bundled into the container.

The hosted catalog uses all formatted item tables pinned in
`website/server/item_review_inventory.json`. Refresh its revisions and row counts
with `python -m website.server.item_review_catalog`. The demo selects up to 50
distinct items per benchmark collection with a fixed seed. Prepare that cache
with `python -m website.server.item_review_sample`; it is also prepared on demand
before model calls. Item tables are read using HTTP ranges. Selected dataset
evidence is cached in `WEBSITE_DATA_DIR/item-review-samples/`, with no provider keys
or deployment descriptions. The first preparation needs temporary disk for a
per-benchmark source index. No dataset content or local CLI artifacts are bundled
into the image. Temporary assessment files expire one hour after a run ends and
are deleted on normal shutdown. Provision writable disk for the reusable sample
cache and temporary results. Reviews do not resume after a restart.
The existing Caliper database and retention behavior are unchanged.

Cold sample preparation can use several GB of RAM while decoding large Parquet
row groups. On a small hosted service, prepare the sample on a machine with enough
memory and privately copy the resulting `item-review-samples/` cache into the
service's data directory before starting reviews. Use the same pinned inventory
and sampling version. Cached reviews read only the selected items. Keep this
gated dataset cache out of Git and public static assets.

After deploying, verify the chooser, both workflows, and the catalog:

```bash
curl -f https://aimslab.stanford.edu/benchmark-caliper/healthz
curl -f https://aimslab.stanford.edu/benchmark-caliper/api/item-review/catalog
```

Open `/benchmark-caliper/`, `/benchmark-caliper/caliper`, and
`/benchmark-caliper/items` in the browser. Run a small real assessment with your
own key, stopping when enough items have been judged, to validate account/model
access and judge quality; automated tests use
mocked OpenAI responses and do not establish scoring quality.

## Render

The repo root ships a `render.yaml` Blueprint that captures the whole service
(Docker, persistent disk, health check, env vars). The easy path:

1. In Render: **New > Blueprint**, pick the `aims-foundations/benchmark-caliper` repo.
2. Render reads `render.yaml` and proposes the `benchmark-caliper` web service.
3. Set `HF_TOKEN` for item-review dataset access. The Blueprint also prompts for
   the optional email values `RESEND_API_KEY`, `RESEND_FROM`, and `FEEDBACK_TO`.
   The app runs without email credentials (email falls back to a dry-run), so
   those can be added later.
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
settings listed above, and set the same env vars, the `HF_TOKEN` secret, and any
optional email credentials. Be sure to set the **Health Check Path** to `/healthz`.

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
