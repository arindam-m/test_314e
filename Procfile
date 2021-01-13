release: python manage.py migrate --noinput
web: gunicorn project_main.wsgi
worker: celery -A project_main worker --beat