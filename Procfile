release: python manage.py collectstatic -y && python manage.py makemigrations && python manage.py migrate
web: gunicorn Bicycle_parking.wsgi
