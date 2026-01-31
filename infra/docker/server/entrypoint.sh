#!/bin/sh
celery -A swippter.celery worker --pool=solo --detach --loglevel=info
python manage.py makemigrations app
python manage.py migrate app
python manage.py makemigrations
python manage.py migrate
python manage.py create_admin
python manage.py collectstatic --no-input
export DJANGO_SETTINGS_MODULE=swippter.settings
opentelemetry-instrument gunicorn swippter.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4 --preload