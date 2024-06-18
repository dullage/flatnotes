#!/bin/sh

curl -f http://localhost:${FLATNOTES_PORT}${FLATNOTES_PATH_PREFIX}/health || exit 1
