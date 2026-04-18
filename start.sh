#!/usr/bin/env bash
set -o errexit

python manage.py migrate --noinput

if [ "${LOAD_FIXTURE_ON_DEPLOY:-false}" = "true" ]; then
  if [ -s core/fixtures/content.json ] && [ "$(tr -d '[:space:]' < core/fixtures/content.json)" != "[]" ]; then
    python manage.py loaddata core/fixtures/content.json
  else
    python manage.py seed_data
  fi
fi

python manage.py create_admin_if_missing
python manage.py refresh_content_snapshot --safe

exec gunicorn plit99_project.wsgi:application \
  --bind 0.0.0.0:${PORT:-10000} \
  --workers ${WEB_CONCURRENCY:-1} \
  --timeout ${GUNICORN_TIMEOUT:-120}
