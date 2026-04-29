#!/usr/bin/env bash
set -o errexit

if [ -f ".env" ]; then
  set -o allexport
  source ".env"
  set +o allexport
fi

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py check
python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput
