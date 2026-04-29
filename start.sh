#!/usr/bin/env bash
set -o errexit

if [ -f ".env" ]; then
  set -o allexport
  source ".env"
  set +o allexport
fi

PORT="${PORT:-${WAITRESS_PORT:-8000}}"
THREADS="${WAITRESS_THREADS:-4}"

python manage.py migrate --noinput
python manage.py create_admin_if_missing

waitress-serve --listen="0.0.0.0:${PORT}" --threads="${THREADS}" plit99_project.wsgi:application
