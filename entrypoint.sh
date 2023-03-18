#!/bin/bash

set -e

USERNAME=flatnotes

echo Setting up user and group...
addgroup \
  --gid ${PGID} \
  ${USERNAME} \
  || echo "Group '${PGID}' already exists."

adduser \
  --disabled-password \
  --gecos "" \
  --uid ${PUID} \
  --gid ${PGID} \
  ${USERNAME} \
  || echo "User '${PUID}' already exists."

echo Setting file permissions...
chown -R ${PUID}:${PGID} ${FLATNOTES_PATH}

echo Starting flatnotes...
cd ${APP_PATH}
exec gosu ${PUID}:${GUID} \
  python -m \
  uvicorn \
  main:app \
  --app-dir flatnotes \
  --host 0.0.0.0 \
  --port 8080
