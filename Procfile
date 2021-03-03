web: uwsgi uwsgi.ini
worker: celery -A apps worker -l info --concurrency=2 -B
