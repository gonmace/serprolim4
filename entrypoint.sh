#!/bin/sh

echo 'Running collectstatic...'
python manage.py collectstatic --noinput --settings=main.prod

echo 'Running migrations...'
python manage.py migrate --settings=main.prod

echo 'Runing Server...'
gunicorn main.wsgi:application DJANGO_SETTINGS_MODULE=main.prod --bind 0.0.0.0:8000