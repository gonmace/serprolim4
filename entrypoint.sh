#!/bin/sh

echo 'Running collectstatic...'
python manage.py collectstatic --noinput --settings=core.prod

echo 'Running migrations...'
python manage.py migrate --settings=core.prod

echo 'Starting gunicorn...'
DJANGO_SETTINGS_MODULE=core.prod gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile -
