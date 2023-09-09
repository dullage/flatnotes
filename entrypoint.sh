#!/bin/bash

echo "WARNING: Breaking changes introduced in version 3.x:"
echo "  - The note directory inside the Docker container has moved from /app/data to simply /data."

if [ `id -u` -eq 0 ] && [ `id -g` -eq 0 ]; then
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
    exec gosu ${PUID}:${PGID} \
      python -m \
      uvicorn \
      main:app \
      --app-dir flatnotes \
      --host 0.0.0.0 \
      --port 8080 \
      --proxy-headers \
      --forwarded-allow-ips "*"
else
    echo "A user was set by docker, skipping permissions setup."
    exec python -m \
      uvicorn \
      main:app \
      --app-dir flatnotes \
      --host 0.0.0.0 \
      --port 8080 \
      --proxy-headers \
      --forwarded-allow-ips "*"
fi
