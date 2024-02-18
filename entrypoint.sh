#!/bin/bash

set -e

flatnotes_command="python -m \
                  uvicorn \
                  main:app \
                  --app-dir server \
                  --host 0.0.0.0 \
                  --port 8080 \
                  --proxy-headers \
                  --forwarded-allow-ips '*'"

if [ `id -u` -eq 0 ] && [ `id -g` -eq 0 ]; then
    echo Setting file permissions...
    chown -R ${PUID}:${PGID} ${FLATNOTES_PATH}

    echo Starting flatnotes as user ${PUID}...
    exec gosu ${PUID}:${PGID} ${flatnotes_command}
      
else
    echo "A user was set by docker, skipping file permission changes."
    echo Starting flatnotes as user $(id -u)...
    exec ${flatnotes_command}
fi
