web: gunicorn election.wsgi
worker: celery -A election worker -l info
release: python manage.py migrate