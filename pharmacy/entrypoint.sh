#!/bin/sh

python manage.py migrate --noinput

python manage.py collectstatic --noinput

gunicorn pharmacy.wsgi:application --bind 0.0.0.0:10000