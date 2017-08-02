web: gunicorn config.wsgi:application
worker: celery worker --app=bike_parking_toronto.taskapp --loglevel=info
