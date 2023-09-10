#!/bin/bash

set -e

echo "WARNING: Breaking changes introduced in version 3.x:"
echo "  - The port flatnotes uses inside the Docker container has been changed to 8080 (previously 80)."
echo "  - To accompany the above change, support for the PORT environment variable has been removed."
echo "  - The note directory inside the Docker container has moved from /app/data to simply /data."

flatnotes_command="python -m \
                  uvicorn \
                  main:app \
                  --app-dir flatnotes \
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
