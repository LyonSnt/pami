#!/bin/sh
set -eu

python manage.py migrate --noinput
python manage.py collectstatic --noinput --ignore css/input.css

exec "$@"
