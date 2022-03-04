release: python manage.py migrate
web: daphne source.asgi:application --port $PORT --bind 0.0.0.0 -v2
celeryworker2: celery -A source.celery worker & celery -A source beat -l INFO & wait -n
