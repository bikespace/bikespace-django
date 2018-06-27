release: python manage.py collectstatic --noinput -i sw.js && python manage.py makemigrations && python manage.py migrate
web: gunicorn Bicycle_parking.wsgi
