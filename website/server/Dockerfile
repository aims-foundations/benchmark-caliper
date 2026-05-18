# Backend image: FastAPI + uvicorn.
#
# Build context is the repository root (one level above `website/`) so we
# can copy `anthropic_api_package/` for prompts and ICL templates the
# website reads at runtime.

FROM python:3.12-slim

WORKDIR /app

# Install Python deps first so they cache when only source changes.
COPY website/server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# The backend imports prompts + ICL YAMLs from anthropic_api_package/.
# Copy only what's needed — no unrelated CLI artifacts.
COPY anthropic_api_package/prompts/         /app/anthropic_api_package/prompts/
COPY anthropic_api_package/benchmarks/      /app/anthropic_api_package/benchmarks/
COPY anthropic_api_package/regions/         /app/anthropic_api_package/regions/
COPY anthropic_api_package/framework.yaml   /app/anthropic_api_package/framework.yaml

# The website code itself.
COPY website/__init__.py    /app/website/__init__.py
COPY website/server/        /app/website/server/

# Persistent data lives under /app/website/server/data — mount a volume
# to keep it across container restarts.
RUN mkdir -p /app/website/server/data

# Run as a non-root user. Anything that escapes from the Python process
# only has unprivileged FS access. The data dir is chown'd so SQLite +
# blob writes still work.
RUN useradd --create-home --shell /usr/sbin/nologin --uid 10001 webuser \
    && chown -R webuser:webuser /app
USER webuser

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

# Allow the frontend dev container to reach us during local development.
# In production this is overridden via the WEBSITE_ALLOWED_ORIGINS env var.
ENV WEBSITE_ALLOWED_ORIGINS=http://localhost:5173

CMD ["uvicorn", "website.server.app:app", "--host", "0.0.0.0", "--port", "8000"]