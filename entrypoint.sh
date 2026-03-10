#!/bin/sh

echo 'Running collectstatic...'
python manage.py collectstatic --noinput --settings=core.prod

echo 'Running migrations...'
python manage.py migrate --settings=core.prod

echo 'Runing Server...'
gunicorn core.wsgi:application DJANGO_SETTINGS_MODULE=core.prod --bind 0.0.0.0:8000