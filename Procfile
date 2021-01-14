release: python manage.py migrate
web: gunicorn project_main.wsgi
worker: celery -A project_main worker -l INFO