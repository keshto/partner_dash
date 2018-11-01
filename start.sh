#!/bin/bash

: "${SLACK_CLIENT_ID:?needs to be exported}"
: "${SLACK_CLIENT_SECRET:?needs to be exported}"

if [ ! -d ".venv" ]; then
  virtualenv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
else
  source .venv/bin/activate
fi

python manage.py makemigrations
python manage.py migrate
python manage.py runserver