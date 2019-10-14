rm -rf static/jsi18n
django-admin makemessages -a
django-admin makemessages -d djangojs -a
django-admin compilemessages
python manage.py compilejsi18n -l ko-KR
