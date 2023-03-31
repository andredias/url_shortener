#!/bin/bash
set -euo pipefail

if [ "${ENV:-production}" != 'production' ]; then
    python migrate_database.py
fi

exec hypercorn --config=hypercorn.toml url_shortener.main:app
