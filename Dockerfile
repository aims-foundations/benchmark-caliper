# node:24 ships npm 11, which correctly skips esbuild's foreign-platform
# optional packages during `npm ci`. npm 10 (node:20) raises EBADPLATFORM.
FROM node:24-bookworm-slim AS client-build

WORKDIR /app/website/client
COPY website/client/package*.json ./
RUN npm ci

COPY website/client ./
ARG WEBSITE_BASE_PATH=/benchmark-caliper
ENV WEBSITE_BASE_PATH=${WEBSITE_BASE_PATH}
RUN npm run build


FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    WEBSITE_DATA_DIR=/data

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      build-essential \
      fonts-freefont-ttf \
    && rm -rf /var/lib/apt/lists/*

COPY website/server/requirements.txt /tmp/server-requirements.txt
COPY anthropic_api_package_release/requirements.txt /tmp/release-requirements.txt
RUN pip install --no-cache-dir \
    -r /tmp/server-requirements.txt \
    -r /tmp/release-requirements.txt

COPY . .
COPY --from=client-build /app/website/client/dist /app/website/client/dist

RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /app /data

USER appuser
EXPOSE 8000

CMD ["sh", "-c", "uvicorn website.server.app:app --host 0.0.0.0 --port ${PORT:-8000}"]
