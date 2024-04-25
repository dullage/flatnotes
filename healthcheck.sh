#!/bin/sh

curl -f http://localhost:${FLATNOTES_PORT}/health || exit 1
