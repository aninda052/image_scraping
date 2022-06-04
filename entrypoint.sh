#!/bin/bash

python manage.py makemigrations
python manage.py makemigrations scraping
python manage.py migrate --no-input

python manage.py process_tasks &
gunicorn image_scraping.wsgi:application -w 3 --bind 0.0.0.0:8000