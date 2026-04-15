#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

if [ "${LOAD_FIXTURE_ON_DEPLOY:-false}" = "true" ]; then
  python manage.py loaddata core/fixtures/content.json
fi
