#!/bin/bash
# Rebuild static assets and reload the app. Safe to re-run.
# Frontend less/riot compilation now happens through django-compressor
# (COMPRESS_PRECOMPILERS in settings), so the old gulp / .dev steps are gone.
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$DIR/.." && pwd )"
PY="$PROJECT_ROOT/.venv/bin/python"

cd "$PROJECT_ROOT"

"$PY" manage.py collectstatic --noinput > /dev/null
"$PY" manage.py compress > /dev/null

bash "$DIR/uwsgi.sh"
