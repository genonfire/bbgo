#! /bin/bash
find . -name \*.pyc -delete
export DJANGO_DEBUG="Debug"
python manage.py runserver
