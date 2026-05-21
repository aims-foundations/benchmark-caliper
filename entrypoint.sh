#!/bin/sh
# Container entrypoint.
#
# Render attaches the persistent disk to WEBSITE_DATA_DIR at *runtime*, after
# the image is built, and the mount can land owned by root. The app runs as
# the unprivileged "appuser", so we fix ownership here (while still root) and
# then drop privileges with gosu before exec'ing the server.
set -e

DATA_DIR="${WEBSITE_DATA_DIR:-/data}"

if [ "$(id -u)" = "0" ]; then
    mkdir -p "$DATA_DIR"
    chown -R appuser:appuser "$DATA_DIR"
    exec gosu appuser "$@"
fi

# Already unprivileged (e.g. local `docker run --user`): just exec.
exec "$@"
