#!/usr/bin/env bash
set -o errexit

if [ "${ENABLE_DATABASE:-true}" = "true" ] && [ "${BOOTSTRAP_DATABASE:-true}" = "true" ]; then
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
else
  if [ "${ENABLE_DATABASE:-true}" != "true" ]; then
    echo "ENABLE_DATABASE=false: database disabled, skipping migrate, admin bootstrap, and snapshot refresh."
  else
    echo "BOOTSTRAP_DATABASE=false: skipping migrate, admin bootstrap, and snapshot refresh."
  fi
fi

exec gunicorn plit99_project.wsgi:application \
  --bind 0.0.0.0:${PORT:-10000} \
  --workers ${WEB_CONCURRENCY:-1} \
  --timeout ${GUNICORN_TIMEOUT:-120}
