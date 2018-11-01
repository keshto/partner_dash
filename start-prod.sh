#!/bin/bash

# Check if production env var is set
: "${PARTNER_DASH_PROD:?not set}"

# Look for server secret key. This needs to be consistent for prod
: "${SECRET_KEY:?not set and value needs to be kept in a secure location}"

# Values of which slack app it is using for auth
: "${SLACK_CLIENT_ID:?needs to be exported}"
: "${SLACK_CLIENT_SECRET:?needs to be exported}"

if [ ! -d ".venv" ]; then
  virtualenv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
else
  source .venv/bin/activate
fi

python manage.py check --deploy
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8080