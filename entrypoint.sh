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

echo "WARNING: Breaking changes introduced in version 3.x:"
echo "  - The port flatnotes uses inside the Docker container has been changed to 8080 (previously 80)."
echo "  - To accompany the above change, support for the PORT environment variable has been removed."
echo "  - The note directory inside the Docker container has moved from /app/data to simply /data."

echo Starting flatnotes...
cd ${APP_PATH}
exec gosu ${PUID}:${PGID} \
  python -m \
  uvicorn \
  main:app \
  --app-dir flatnotes \
  --host 0.0.0.0 \
  --port 8080
